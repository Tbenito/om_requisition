from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class Requisition(models.Model):

    _name = 'requisition.requisition'
    _description = 'Requisition'
    _inherit = "mail.thread","mail.activity.mixin"
    _rec_name = 'id'

    name = fields.Char(string='Requisition number', tracking=True, default=_rec_name)
    description = fields.Text(string='Description', tracking=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([('draft','Draft'),
                              ('confirmed','Confirmed'),
                              ('approved','Approved'),
                              ('done','Done'),
                              ('canceled','Canceled'),
                              ('refused','Refused')], string='State', default='draft', required=True, tracking=True)
    applicant_id = fields.Many2one('res.users', string='Applicant', default=lambda self: self.env.user)

    def _get_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id
    employee_id = fields.Many2one('hr.employee', string='Employé', default=_get_employee_id, readonly=True)
    applicant_department_id = fields.Many2one(string='Applicant department', related='employee_id.department_id', readonly=True, tracking=True)
    department_head_id = fields.Many2one(related="employee_id.parent_id", string='Department head', readonly=True, tracking=True)
    date = fields.Date(string='Requisition date', tracking=True, readonly=True, default=datetime.now())
    delay = fields.Integer(string='Expected delay', tracking=True)
    delivery_date = fields.Date(string='Delivery date', compute='_compute_delivery_date', tracking=True, required=True)
    transfer_count = fields.Integer(string='Number of transfers', tracking=True)
    transfer_ids = fields.One2many('stock.picking','requisition_requisition_id', string='Transfert')
    purchase_agreement_count = fields.Integer(string='Purchase requisitions', tracking=True)
    purchase_order_count = fields.Integer(string='Purchase orders', tracking=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    company_id = fields.Many2one(related="employee_id.company_id", string='Company', readonly=True, tracking=True)

    state_changes_ids = fields.One2many('requisition.state', 'requisition_id', string='State Changes')
    requisition_line_ids = fields.One2many('requisition.line', 'requisition_id')
    process_pilot_list = fields.Many2many('hr.employee', string='Process Pilot List')

    @api.depends("date")
    def _compute_delivery_date(self):
        for record in self:
            record.delivery_date = record.date + timedelta(days=record.delay)

    def action_view_transfers(self):
        return

    def action_view_agreements(self):
        return

    def action_view_purchase_orders(self):
        return

    def action_confirm(self):
        self.state = 'confirmed'

    def action_approve(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'
        record = self.requisition_line_ids
        for i in range(len(record)):
            record.state = 'approved'
            if record[i].route == 'transfert':
                self.transfer_count += 1
            elif record[i].route == 'purchase':
                self.purchase_order_count += 1

        for line in self:
            if not line.requisition_line_ids:
                raise UserError(_('Please create some product lines.'))
            if not self.transfer_count:
                raise UserError(_('Please Validate the form.'))
            if not self.transfer_ids:
                print('cest bon la !!!!!!!!!!!!!!!!!!!!!!!')

    def action_cancel(self):
        self.state = 'canceled'

    def action_draft(self):
        self.state = 'draft'

    def action_refuse(self):
        self.state = 'refused'

