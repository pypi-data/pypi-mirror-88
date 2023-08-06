from odoo import models


class AccountBankingMandate(models.Model):
    """SEPA Direct Debit Mandate"""
    _inherit = 'account.banking.mandate'

    def name_get(self):
        result = []
        for mandate in self:
            name = mandate.unique_mandate_reference
            acc_number = mandate.partner_bank_id.acc_number
            if acc_number:
                name = '{} [{}]'.format(name, acc_number)
            result.append((mandate.id, name))
        return result
