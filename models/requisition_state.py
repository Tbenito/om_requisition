
from odoo import models, fields, api
from datetime import datetime, date, timedelta


class RequisitionState(models.Model):

    _name = 'requisition.state'
    _description = 'Requisition State'

    name = fields.Char()
    date = fields.Datetime('Date')
    user_id = fields.Many2one('res.users')
    old_state = fields.Char('From state')
    new_state = fields.Char('To state')
    requisition_id = fields.Many2one('requisition.requisition', string='Requisition')