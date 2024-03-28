from odoo import api, fields, models


class MillSources(models.Model):
    _name = 'mill.sources'
    _description = "Mill Sources"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner', string="Customer", tracking=True)
    source_datetime = fields.Datetime(string="Date", default=fields.Datetime.now)
    img = fields.Image(string="Image", readonly=True, compute="_compute_img")

    customer_prod_ids = fields.One2many('customer.products','source_id',string = "Product")

    state = fields.Selection([('New', 'New'),
                              ('Done', 'Done'),
                              ('Cancel', 'Cancel')], string="State",default="New", search = "_search_state")

    ref = fields.Char(string="Source Reference", readonly=True)

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('sources.sequence')
        return super(MillSources, self).create(vals)

    @api.depends('customer_id')
    def _compute_img(self):
        for rec in self:
            rec.img = rec.customer_id.image_1920

    def action_set_Done_state(self):
        for rec in self:
            rec.state = 'Done'

    def action_set_Cancel_state(self):
        for rec in self:
            rec.state = "Cancel"


    @api.model
    def name_get(self):
        name_list = []
        for rec in self:
            name = "[" + str(rec.customer_id.vat) + "]" + " " + str(rec.customer_id.name)
            name_list.append((rec.id,name))
        return name_list

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('state', operator, name), ('customer_prod_ids.product_id', operator, name)]
        return self._search(domain + args, limit=limit, access_right_uid=name_get_uid)




    #_rec_name = "combined_name"

    #combined_name = fields.Char(compute="_compute_combined_name")

    #@api.depends('customer_id')
    #def _compute_combined_name(self):
    #    for rec in self:
    #        rec.combined_name = "[" + str(rec.customer_id.vat) + "]" + " " + str(rec.customer_id.name)
