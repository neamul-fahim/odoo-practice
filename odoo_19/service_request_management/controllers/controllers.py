# from odoo import http


# class ServiceRequestManagement(http.Controller):
#     @http.route('/service_request_management/service_request_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/service_request_management/service_request_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('service_request_management.listing', {
#             'root': '/service_request_management/service_request_management',
#             'objects': http.request.env['service_request_management.service_request_management'].search([]),
#         })

#     @http.route('/service_request_management/service_request_management/objects/<model("service_request_management.service_request_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('service_request_management.object', {
#             'object': obj
#         })

