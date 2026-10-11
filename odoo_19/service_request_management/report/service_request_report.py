from odoo import api, fields, models, _

class ServiceRequestReport(models.AbstractModel):
    _name = 'report.service_request_management.ser_req_report_template'
    _description = 'Service Request Report Template'

    def _get_report_values(self, docids, data=None):
        data = data or {}

        date_from = fields.Date.from_string(data['date_from'])
        date_to = fields.Date.from_string(data['date_to'])
        state = data['state']

        return {
            "date_from": date_from,
            "date_to": date_to,
            "state": state,
        }
