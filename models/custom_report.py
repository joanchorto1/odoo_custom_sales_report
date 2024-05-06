from odoo import models, fields, api

class CustomSalesReport(models.Model):
    _name = 'custom.sales.report'
    _description = 'Custom Sales Report'
    _auto = False  # This is important to indicate that this model is not managed by Odoo (no table creation)

    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='State', readonly=True)
    state_count = fields.Integer(string='State Count', readonly=True)
    total_amount = fields.Float(string='Total Amount', readonly=True)

    def init(self):
        # Execute SQL query to create the view
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW custom_sales_report AS
                SELECT
                    row_number() OVER () AS id,
                    so.user_id AS user_id,
                    so.state AS state,
                    COUNT(so.id) AS state_count,
                    SUM(so.amount_total) AS total_amount
                FROM
                    sale_order so
                GROUP BY
                    so.user_id, so.state
        ''')

    def get_state_display(self, state):
        return dict(self._fields['state'].selection).get(state)