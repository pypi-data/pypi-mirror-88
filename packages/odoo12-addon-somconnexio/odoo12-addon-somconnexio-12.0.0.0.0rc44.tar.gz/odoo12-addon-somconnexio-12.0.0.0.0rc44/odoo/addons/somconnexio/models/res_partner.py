from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.queue_job.job import job

from odoo.addons.somconnexio.somoffice.user import SomOfficeUser


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )
    coop_agreement = fields.Boolean(string="Has cooperator agreement?",
                                    compute="_compute_coop_agreement",
                                    store=True,
                                    readonly=True)
    cooperator_end_date = fields.Date(string="Cooperator End Date")
    volunteer = fields.Boolean(string="Volunteer")
    type = fields.Selection(selection_add=[
        ('service', 'Service Address'),
        ('contract-email', 'Contract Email')
    ])
    nationality = fields.Many2one('res.country', 'Nacionality')

    contract_ids = fields.One2many(string="Contracts",
                                          comodel_name="contract.contract",
                                          inverse_name="partner_id")
    full_street = fields.Char(
        compute='_get_full_street',
        store=True
    )
    sc_effective_date = fields.Date('Somconnexio Effective Date')
    sc_cooperator_end_date = fields.Date('Somconnexio Cooperator End Date')
    sc_cooperator_register_number = fields.Integer('Somconnexio Cooperator Number')

    @api.model
    def _name_search(
        self, name, args=None, operator='ilike', limit=100, name_get_uid=None
    ):
        if ['customer', '=', True] in args and ['parent_id', '=', False] in args:
            args = [
                arg for arg in args
                if arg != ['customer', '=', True] and arg != ['parent_id', '=', False]
            ]
            custom_search = True
        else:
            custom_search = False
        result = super()._name_search(
            name=name, args=args, operator=operator,
            limit=limit, name_get_uid=name_get_uid
        )
        if not custom_search:
            return result
        partner_ids = []
        for r in result:
            partner = self.browse(r[0])
            if partner.type == 'contract-email':
                if partner.parent_id.customer:
                    partner_ids.append(partner.parent_id.id)
            else:
                if not partner.parent_id and partner.customer:
                    partner_ids.append(r[0])
        if partner_ids:
            partner_ids = list(set(partner_ids))
            result = models.lazy_name_get(self.browse(partner_ids))
        else:
            result = []
        return result

    @api.multi
    def get_available_email_ids(self):
        self.ensure_one()
        email_id_list = [self.id] if self.email else []
        email_id_obj = self.env['res.partner'].search(
            [('parent_id', '=', self.id),
             ('type', '=', 'contract-email')
             ]
        )
        for data in email_id_obj:
            email_id_list.append(data.id)
        return email_id_list

    def _get_name(self):
        if 'email_tags' in self.env.context:
            return self.email
        if self.type == 'service':
            self.name = dict(self.fields_get(['type'])['type']['selection'])[self.type]
        res = super()._get_name()
        return res

    @api.multi
    @api.depends("sponsor_id", "coop_agreement_id")
    @api.depends("subscription_request_ids.state")
    def _compute_coop_candidate(self):
        for partner in self:
            if partner.member:
                is_candidate = False
            else:
                sub_requests = partner.subscription_request_ids.filtered(
                    lambda record: (
                        record.state == 'done' and
                        not record.sponsor_id and
                        not record.coop_agreement_id
                    )
                )
                is_candidate = bool(sub_requests)
            partner.coop_candidate = is_candidate

    @api.multi
    @api.depends("sponsor_id", "coop_agreement_id")
    def _compute_coop_agreement(self):
        for partner in self:
            if partner.coop_agreement_id:
                partner.coop_agreement = True
            else:
                partner.coop_agreement = False

    @api.one
    @api.constrains('child_ids')
    def _check_invoice_address(self):
        invoice_addresses = self.env['res.partner'].search([
            ('parent_id', '=', self.id),
            ('type', '=', 'invoice')
        ])
        if len(invoice_addresses) > 1:
            raise ValidationError(
                'More than one Invoice address by partner is not allowed'
            )

    def _set_contract_emails_vals(self, vals):
        new_vals = {}
        if 'parent_id' in vals:
            new_vals['parent_id'] = vals['parent_id']
        if 'email' in vals:
            new_vals['email'] = vals['email']
        new_vals['type'] = 'contract-email'
        new_vals['customer'] = False
        return new_vals

    @api.depends('street', 'street2')
    def _get_full_street(self):
        for record in self:
            if record.street2:
                record.full_street = "{} {}".format(record.street, record.street2)
            else:
                record.full_street = record.street

    @job
    def create_user(self, partner):
        SomOfficeUser(
            partner.ref,
            partner.email,
            partner.vat,
        ).create()

    @api.model
    def create(self, vals):
        if "ref" not in vals:
            vals['ref'] = self.env.ref(
                "somconnexio.sequence_partner"
            ).next_by_id()

        if 'type' in vals and vals['type'] == 'contract-email':
            vals = self._set_contract_emails_vals(vals)
        return super().create(vals)

    def write(self, vals):
        if 'type' in vals and vals['type'] == 'contract-email':
            vals = self._set_contract_emails_vals(vals)
            for partner in self:
                partner.name = False
                partner.street = False
                partner.street2 = False
                partner.city = False
                partner.state_id = False
                partner.country_id = False
                partner.customer = False
        super().write(vals)
        return True
