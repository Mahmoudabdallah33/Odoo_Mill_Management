from odoo import api, fields, models

class CustomerProducts(models.Model):
    _name = "customer.products"
    _description = "Owen Product of the Customer"
    _rec_name = "product_id"


    product_id = fields.Many2one('product.product', string="Product")

    price = fields.Float(string="Price")

    weight = fields.Float(string="Product Weight")

    source_id = fields.Many2one('mill.sources', string="Sources")
