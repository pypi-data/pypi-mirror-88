import logging
from odoo.addons.component.core import Component
from . import schemas
from werkzeug.exceptions import BadRequest
from odoo.addons.base_rest.http import wrapJsonException
import json
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class AccountInvoiceService(Component):
    _inherit = "account.invoice.service"

    def create(self, **params):
        params = self._prepare_create(params)
        # tracking_disable=True in context is needed
        # to avoid to send a mail in Account Invoice creation
        invoice = self.env["account.invoice"].with_context(
            tracking_disable=True
        ).create(params)
        return self._to_dict(invoice)

    def _validator_create(self):
        return schemas.S_ACCOUNT_INVOICE_CREATE

    def _validator_return_create(self):
        return schemas.S_ACCOUNT_INVOICE_RETURN_CREATE

    def _prepare_create_line(self, line):
        account = self.env['account.account'].search(
            [('code', '=', line['accountingCode'])]
        )
        if not account:
            raise wrapJsonException(
                BadRequest(
                    'Account code %s not found' % (
                        line['accountingCode']
                    )
                )
            )
        tax = self.env['account.tax'].search(
            [('oc_code', '=', line['taxCode'])]
        )
        if not tax:
            raise wrapJsonException(
                BadRequest(
                    'Tax code %s not found' % (
                        line['taxCode']
                    )
                )
            )
        product_id = self.env['product.product'].search(
            [('default_code', '=', line['invoiceSubCategoryCode'])]
        ).id
        if not product_id:
            raise wrapJsonException(
                BadRequest(
                    'Product with code %s not found' % (
                        line['invoiceSubCategoryCode'],)
                )
            )
        response_line = {
            'name': line['description'],
            'account_id': account.id,
            'oc_amount_taxes': line['amountTax'],
            'oc_amount_untaxed': line['amountWithoutTax'],
            'oc_amount_total': line['amountWithTax'],
            "invoice_line_tax_ids": [(4, tax.id, 0)],
            "product_id": product_id
        }
        return response_line

    def _prepare_create(self, params):

        # TODO: Fix this timezone change
        # We have a problem with the timezone.
        # The timestamp getted from the invoice polling is in UTC,
        # and we want save the local date of the invoice.
        # The invoices have the time to 00:00:00 and when OC convert this time to UTC,
        # remove 2 hours and change the day to the previous day. If we add 2 hours,
        # the date is always the local time :D
        # from pytz import timezone
        # localtz = timezone('Europe/Madrid')
        # return localtz.localize(
        #   datetime.fromtimestamp(int(self.opencell_raw_invoice.invoiceDate)/1000)
        # )

        invoice_date = (
            datetime.fromtimestamp(
                int(params['invoiceDate']) / 1000
            ) + timedelta(hours=2)
        ).date()
        account_code = params['billingAccountCode']
        partner_id = int(account_code[0:account_code.index("_")])
        if not self.env['res.partner'].search(
            [('id', '=', partner_id)]
        ):
            raise wrapJsonException(
                BadRequest(
                    'Partner with id %s not found' % (
                        partner_id,)
                )
            )
        invoice_lines = [
            line
            for category in params['categoryInvoiceAgregates']
            for line in category['listSubCategoryInvoiceAgregateDto']
        ]
        lines = [
            self.env['account.invoice.line'].create(
                self._prepare_create_line(line)
            ).id
            for line in invoice_lines
            if 'amountWithoutTax' in line and line['amountWithoutTax']
        ]
        oc_taxes_parsed = params['taxAggregates']
        for oc_tax in oc_taxes_parsed:
            tax = self.env['account.tax'].search([
                ('oc_code', '=', oc_tax['taxCode'])
            ])
            if not tax:
                raise wrapJsonException(
                    BadRequest(
                        'Tax code %s in Tax Aggregate not found' % (
                            oc_tax['taxCode'],)
                    )
                )

        oc_taxes = json.dumps(params['taxAggregates'])
        return {
            "partner_id": partner_id,
            "oc_number": params['invoiceNumber'],
            "date_invoice": invoice_date,
            "oc_untaxed": params['amountWithoutTax'],
            "oc_total": params['amountWithTax'],
            "oc_total_taxed": params['amountTax'],
            "invoice_line_ids": [(6, 0, lines)],
            "oc_taxes": oc_taxes
        }

    @staticmethod
    def _to_dict(account_invoice):
        return {
            "id": account_invoice.id
        }
