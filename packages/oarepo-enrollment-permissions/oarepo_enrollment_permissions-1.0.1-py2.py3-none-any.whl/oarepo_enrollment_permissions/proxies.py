from flask import current_app
from werkzeug.local import LocalProxy

current_enrollment_permissions = LocalProxy(lambda: current_app.extensions['oarepo-enrollment-permissions'])
