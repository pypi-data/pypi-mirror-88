from odoo import models, tools


class PartnerOTRSView(models.Model):
    _name = 'partner.otrs.view'
    _auto = False

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
                %s
            )
        ''' % (
            self._table, self._query()
        ))

    def _query(self):
        return '''
            SELECT DISTINCT ON (partner.id)
                partner.ref AS customerid,
                COALESCE(partner.firstname, '-'::character varying) AS first_name,
                COALESCE(partner.lastname, '-'::character varying) AS name,
                partner.cooperator_register_number,
                partner.effective_date,
                partner.cooperator_end_date,
                CASE
                    WHEN partner.active = true THEN 1
                    WHEN partner.active = false THEN 2
                    ELSE NULL::integer
                END AS active,
                partner.birthdate_date,
                partner.type,
                VAT AS identifier_type,
                partner.vat AS identifier_code,
                partner.email AS email,
                CASE
                    WHEN partner.lang::text = 'ca_ES'::text THEN 'ca'::character varying
                    WHEN partner.lang::text = 'es_ES'::text THEN 'es'::character varying
                    ELSE NULL::character varying
                END AS language,
                partner.street AS address,
                partner.city,
                partner.zip,
                country.code AS country_code,
                country.name AS country,
                state.code AS subdivision_code,
                state.name AS subdivision
            FROM res_partner partner
            LEFT JOIN res_country country ON partner.country_id = country.id
            LEFT JOIN res_country_state state ON partner.state_id = state.id
            WHERE partner.parent_id IS NULL
            ORDER BY partner.id
        '''
