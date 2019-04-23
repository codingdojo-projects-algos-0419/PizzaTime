from config import app
from staff_controller import *

## master routes ##
# Staff Login
app.add_url_rule('/admin', view_func=admin)
app.add_url_rule('/staff/login', view_func=staff_login, methods=["POST"])
app.add_url_rule('/staff', view_func=staff)

# Admin Dashboard

# Kitchen Staff Dashboard
app.add_url_rule('/admin/nav', view_func=admin_nav)
app.add_url_rule('/admin/logout', view_func=admin_logout)
app.add_url_rule('/store/logout', view_func=store_logout)

#3admin and staff routes
app.add_url_rule('/admin/dash', view_func=admin_dash)
app.add_url_rule('/admin/account', view_func=admin_acc)
app.add_url_rule('/account/edit', view_func=admin_edit)
app.add_url_rule('/store', view_func=store)
