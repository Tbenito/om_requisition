
from odoo import models, fields, api


class RequisitionLine(models.Model):
    _name = 'requisition.line'
    _description = 'Requisition Line'

    name = fields.Text(string='Description')
    requisition_id = fields.Many2one('requisition.requisition')
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Quantity')
    product_uom = fields.Many2one(related="product_id.uom_id", string='Unit of Measure')
#     analytic_account_id =
#     analytic_tag_asset_ids =
#     analytic_tag_ids =
    picking_type_id = fields.Many2one('stock.picking.type', string='Operation type')
    route = fields.Selection([('transfert','Transfert'),('purchase','Purchase')], default='transfert', string='Route')
    state = fields.Selection(related='requisition_id.state')
    # state = fields.Selection([('draft', 'Draft'),
    #                           ('confirmed', 'Confirmed'),
    #                           ('approved', 'Approved'),
    #                           ('done', 'Done'),
    #                           ('canceled', 'Canceled'),
    #                           ('refused', 'Refused')], string='State', default='draft')
    qty_to_deliver = fields.Float(string='Qty To Deliver', readonly=True)
    is_qty_available = fields.Boolean(compute="_is_qty_available")
    move_ids = fields.Many2many('stock.move', string="Stock Moves")
    sequence = fields.Integer(string="Sequence")
    display_qty_widget = fields.Boolean(string='Display Qty Widget')
    is_done = fields.Boolean(readonly=True)
    product_type = fields.Selection([('conso', 'Consomable'),
                              ('service', 'Service'),
                              ('stock', 'Article Stockable')], string='State')
    warehouse_id = fields.Many2one("stock.warehouse", string='Warehouse', readonly=True)
    qty_available_today = fields.Float('Qty Available Today', readonly=True)
    virtual_available_at_date = fields.Float(readonly=True)
    free_qty_today = fields.Float(readonly=True)
    scheduled_date = fields.Datetime(readonly=True)
    forecast_expected_date = fields.Datetime(readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)

    @api.onchange('product_id', 'qty')
    def _is_qty_available(self):
        for record in self:
            available_qty = record.product_id.qty_available
            if available_qty >= record.qty:
                record.is_qty_available = True
            else:
                record.is_qty_available = False



