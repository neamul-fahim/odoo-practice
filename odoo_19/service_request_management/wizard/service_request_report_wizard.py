from odoo import fields, models, api, _

class ServiceRequestReportWizard(models.TransientModel):
    _name = "service.request.report.wizard"
    _description = "Service Request Wizard"
    date_from = fields.Datetime(string="Date From (YYYY-MM-DD)")
    date_to = fields.Datetime(string="Date To (YYYY-MM-DD)")
    state = fields.Selection(string="State", selection=lambda self: self.env["service.request"]._fields["state"].selection)

    def generate_report(self):
        self.ensure_one()
        data = {
            "date_from": self.date_from,
            "date_to": self.date_to,
            "state": self.state,
        }

        return self.env.ref("service_request_management.action_service_request_report").report_action(self, data=data)