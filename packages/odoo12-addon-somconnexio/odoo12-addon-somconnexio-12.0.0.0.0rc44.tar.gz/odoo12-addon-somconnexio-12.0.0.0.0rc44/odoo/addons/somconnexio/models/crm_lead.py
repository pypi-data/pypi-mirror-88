from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    subscription_request_id = fields.Many2one(
        'subscription.request', 'Subscription Request'
    )
    iban = fields.Char(string="IBAN")

    mobile_lead_line_id = fields.Many2one(
        'crm.lead.line',
        compute='_compute_mobile_lead_line_id',
        string="Mobile Lead Line",
    )

    # TODO: To modify if in the future we can have more than one `mobile_lead_line_id`
    def _compute_mobile_lead_line_id(self):
        for crm_lead in self:
            for line in crm_lead.lead_line_ids:
                if line.mobile_isp_info:
                    crm_lead.mobile_lead_line_id = line
                    break
