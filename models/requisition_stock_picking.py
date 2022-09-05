from odoo import models, fields, api
from datetime import datetime, timedelta


class RequisitionStockPicking(models.Model):

    _inherit = "stock.picking"


    requisition_requisition_id = fields.Many2one('requisition.requisition')
