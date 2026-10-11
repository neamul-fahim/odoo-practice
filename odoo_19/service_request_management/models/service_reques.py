from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

class ServiceRequest(models.Model):
    _name = "service.request"
    _description = "service request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = "title"
    reference = fields.Char(string="Reference", default="New", readonly=True, copy=False)
    title = fields.Char(string="Title", required=True, default="New")
    requester_id = fields.Many2one(string="Requester", comodel_name="hr.employee")
    requester_department_id = fields.Many2one(string="Requester Department", comodel_name="hr.department",
                                              related="requester_id.department_id")
    assigned_use_id = fields.Many2one(string="Assigned user", comodel_name="res.users")
    request_date = fields.Datetime(string="Request Data", default=fields.Datetime.now, readonly=True, index=True)
    expected_completion_date = fields.Date(string="Expected Completion Date", tracking=True)
    priority = fields.Selection(string="Priority", selection=[
        ("low","Low"), ("medium","Medium"), ("high","High"), ("urgent","Urgent")], default='low')
    description = fields.Text(string="Description")
    tag_ids = fields.Many2many(string="Tags", comodel_name="service.request.tag")
    company_id = fields.Many2one(string="Company", comodel_name="res.company", default=lambda self: self.env.company)
    currency_id = fields.Many2one(string="Currency", comodel_name="res.currency", related="company_id.currency_id", readonly=False)
    estimated_cost = fields.Monetary(string="Estimated Cost", currency_field="currency_id", tracking=True)
    state = fields.Selection(string="State", selection=[
    ("draft", "Draft"),
    ("submitted", "Submitted"),
    ("approved", "Approved"),
    ("in_progress", "In Progress"),
    ("done", "Done"),
    ("canceled", "Canceled"),
    ], default="draft", tracking=True)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id", store=True)
    line_ids = fields.One2many(string="Lines", comodel_name="service.request.line", inverse_name="requester_id")


    @api.depends("line_ids")
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = sum(rec.line_ids.mapped("subtotal"))

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get("reference", "New") == "New":
                val["reference"] = self.env["ir.sequence"].next_by_code("service.request") or "New"
        return super().create(vals_list)



    def action_submit(self):
        self.write({"state":"submitted"})
    def action_approve(self):
        self.write({"state":"approved"})
    def action_in_progress(self):
        self.write({"state":"in_progress"})
    def action_done(self):
        self.write({"state":"done"})
    def action_cancel(self):
        self.write({"state":"canceled"})



class ServiceRequestLine(models.Model):
    _name = "service.request.line"
    _description = "Service Request Line"

    requester_id = fields.Many2one(string="Requester", comodel_name="service.request", required=True)
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    description = fields.Text(string="Description")
    quantity = fields.Integer(string="Quantity", default=1)
    unit_price = fields.Integer(string="Unit Price", compute="_compute_unit_price", readonly=False)
    discount = fields.Float(string="Discount %", default=0)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", inverse="_inverse_subtotal", readonly=False)

    @api.depends("product_id")
    def _compute_unit_price(self):
        for rec in self:
            rec.unit_price = rec.product_id.lst_price

    @api.depends("quantity", "unit_price", "discount")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price * (1-rec.discount/100)

    def _inverse_subtotal(self):
        for rec in self:
            gross = rec.quantity * rec.unit_price

            if gross:

                rec.discount = (1-rec.subtotal/gross) * 100

            else:
                rec.discount = 0

    # inverse doesn't get called on the form while changing value, it acts after saving the record so we made an onchange.
    @api.onchange("subtotal")
    def _onchange_subtotal(self):
        for rec in self:
            rec._inverse_subtotal()



    @api.constrains("quantity", 'discount')
    def _check_constraint(self):
        for rec in self:
            if rec.quantity < 0:
                raise ValidationError("quantity can't be negative")
            if 0 > rec.discount > 100:
                raise ValidationError("discount has to be between 0 and 100")




class ServiceRequestTag(models.Model):
    _name = "service.request.tag"
    _description = "tags"
    name = fields.Char(string="Name")
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "tag name should be unique"
    )