from . import users, appointments, prescriptions, reports, surgery, bills

def init_routes(app):
    users.register_routes(app)
    appointments.register_routes(app)
    prescriptions.register_routes(app)
    reports.register_routes(app)
    surgery.register_routes(app)
    bills.register_routes(app)
