{
    "name": "Credit control dunning fees",
    "version": "16.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainer": "Camptocamp",
    "category": "Accounting",
    "complexity": "normal",
    "depends": ["account_credit_control"],
    "website": "https://github.com/OCA/credit-control",
    "data": [
        "view/policy_view.xml",
        "view/line_view.xml",
        "report/report_credit_control_summary.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "application": False,
}