from config import app
from controllers import *

## master routes ##
# Restaurant Welcome page
app.add_url_rule('/', view_func=index)
# Customer Login
app.add_url_rule('/register', view_func=register)
app.add_url_rule('/user/login', view_func=members)
# Customer Registration
# Customer dashboard
app.add_url_rule('/nav', view_func=nav)
app.add_url_rule('/logout', view_func=logout)

## customer routes
app.add_url_rule('/quick', view_func=quick)
