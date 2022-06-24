{
    'name': "Parking Management",
    'version': '1.0',
    'category': 'Parking',
    'author': "Odoo Master",
    'sequence': -100,
    'summary': 'Parking management system',
    'description': """
    Description text
    """,
    'depends': [
        'mail',
        'product',
        'hr',
        'resource',
        'report_xlsx',
    ],
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/menu.xml',
        'wizard/parking_report_wizard_view.xml',
        'views/parking_lot_view.xml',
        'views/parking_vehicle_view.xml',
        'views/parking_details_view.xml',
        'views/parking_ticket_view.xml',
        'views/parking_pricelist_view.xml',
        'wizard/parking_report_wizard_view.xml',
        'reports/pdf_report.xml',
        'reports/report.xml',

    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
    'auto install': False,
    'license': 'LGPL-3',
}
