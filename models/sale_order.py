from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_email = fields.Char(string='Adreça de correu preferencial del client')
    num_articles = fields.Integer(string='Nombre de articles', compute='_compute_num_articles')

    def _compute_num_articles(self):
        for order in self:
            order.num_articles = len(order.order_line)

