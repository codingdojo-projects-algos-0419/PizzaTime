from config import app
from controllers import *

## master routes ##
app.add_url_rule('/admin', view_func=admin)
app.add_url_rule('/staff', view_func=staff)
app.add_url_rule('/', view_func=index)
app.add_url_rule('/user/login', view_func=members)
app.add_url_rule('/nav', view_func=nav)
app.add_url_rule('/admin/nav', view_func=admin_nav)
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/admin/logout', view_func=admin_logout)
app.add_url_rule('/store/logout', view_func=store_logout)

#3admin and staff routes
app.add_url_rule('/admin/dash', view_func=admin_dash)
app.add_url_rule('/admin/account', view_func=admin_acc)
app.add_url_rule('/store', view_func=store)

## customer routes
app.add_url_rule('/quick', view_func=quick)
