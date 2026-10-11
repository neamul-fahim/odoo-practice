from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class ServiceRequest(models.Model):
    _name = "service.request"
    _description = "Service Request"
    _order = "request_date desc, id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default="/",
        index=True,
    )
    title = fields.Char(required=True, index=True)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        default=lambda self: self.env.user.partner_id,
        index=True,
        ondelete="restrict",
    )
    description = fields.Text()
    request_date = fields.Date(
        string="Request Date",
        required=True,
        default=fields.Date.context_today,
        index=True,
    )
    priority = fields.Selection(
        selection=[
            ("low", "Low"),
            ("normal", "Normal"),
            ("high", "High"),
        ],
        required=True,
        default="normal",
        index=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="draft",
        copy=False,
        index=True,
    )
    attachment = fields.Binary(attachment=True)
    attachment_filename = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        portal_only = (
            self.env.user.has_group("base.group_portal")
            and not self.env.user.has_group("base.group_user")
        )
        for vals in vals_list:
            if portal_only:
                # A portal caller cannot choose another owner or submit a
                # request directly in a staff-only/final state.
                vals["partner_id"] = self.env.user.partner_id.id
                if vals.get("state", "draft") not in ("draft", "submitted"):
                    raise AccessError(
                        _("Portal users can only create draft or submitted requests.")
                    )
            # References are always assigned server-side, even if a caller
            # supplies a value for the readonly field.
            vals["name"] = sequence.next_by_code("service.request") or "/"
        return super().create(vals_list)
