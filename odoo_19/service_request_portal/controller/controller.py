from odoo import http
from odoo.http import request, Controller


class Portal(Controller):

    def get_service_requests(self, domain, limit, offset):

        sr_object = request.env["service.request"]
        sr = sr_object.search(domain, limit=limit, offset=offset)
        return sr


    @http.route("/home", auth="user", type="http")
    def my(self, **kwargs):
        priority = kwargs.get("priority")
        search = kwargs.get("search_text")
        domain = []
        if search:
            domain.append(("title", "ilike", search))
        if priority:
            domain.append(("priority", "ilike", priority))

        print(f'domain ================================================== {domain}')
        sr_object = request.env["service.request"]
        total_count = sr_object.search_count(domain)

        input_page_number = kwargs.get("input_page_number", None)

        try:
            limit = int(kwargs.get("limit", 10))
        except:
            limit = 15
        page_count = (total_count // limit)+1 if (total_count % limit) !=0 else (total_count // limit)

        try:
            page = int(input_page_number if input_page_number else kwargs.get("page", 1))
        except:
            page = 1

        page = max(1, min(page, page_count))
        offset = (page - 1) * limit



        sr = self.get_service_requests(domain, limit, offset)




        data = {
            "sr": sr,
            "page": page,
            "page_count": page_count,
            "priorities": ["Low", "Normal", "High"],
            "search_text": search,
            "priority": priority,
        }
        return request.render("service_request_portal.home_page", data)