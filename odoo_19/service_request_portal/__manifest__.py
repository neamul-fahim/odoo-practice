{
    "name": "Service Request Portal",
    "summary": "Service request records for the portal practice exercise",
    "description": "Backend model and access foundation for the Service Request Portal exercise.",
    "category": "Services",
    "version": "19.0.1.0.0",
    "depends": ["base", "portal"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/service_request_sequence.xml",
        "views/service_request_views.xml",

        #template
        "views/templates/home_page.xml",
        "views/templates/service_request_table.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
