from flask import render_template, redirect, request, session, flash
from config import db, datetime
from models import *
from staff_model import Staff
from flask_socketio import SocketIO,emit

## render admin/staff login page
def admin():
    return render_template('admin.html')

def staff_login():
    # print(' staff_login '*20)
    employee=Staff.validate_login(request.form)
    # print('*'*80,employee)
    if employee:
        session['employee_id']=employee.id
        session['user_name']=employee.first_name+' '+employee.last_name
        session['login_session']=Staff.get_session_key(employee.id)
        if employee.user_level<6:
            return redirect('/store')
        if employee.user_level>=6:
            return redirect('/admin/dash')
    return redirect('/admin')

#render admin dashboard
def admin_dash():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/store')
    topping_menu=ToppingMenu.get_all()
    sizes=Size.get_all()
    styles=Style.get_all()
    order_types=OrderType.get_all()
    return render_template('admindash.html',topping_menu=topping_menu,sizes=sizes,styles=styles, order_types=order_types)

def create_topping():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    print(request.form)
    new_topping=ToppingMenu.new(request.form['top_name'],request.form['description'],request.form['price'])
    # maybe change to Ajax partial:
    # return render_template('topping_menu_item.html',topping=new_topping)
    return redirect('/admin/dash')

def get_topping(id):
    topping=ToppingMenu.query.get(id)
    return render_template('top.html', topping = topping)

def update_topping(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    print(request.form)
    topping=ToppingMenu.query.get(id)
    topping.update(request.form)
    return redirect('/admin/dash#tabs-1')

def update_topping_availability():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    print(request.form)
    return Topping.set_availability(request.form['topping_id'],request.form['availability'])

def create_style():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    print(request.form)
    new_style=Style.new(request.form['name'],request.form['description'],request.form['price'])
    return redirect('/admin/dash#tabs-2')

def get_style(id):
    style=Style.query.get(id)
    return render_template('style.html', style = style)

def update_style(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    style=Style.query.get(id)
    style.update(request.form)
    return redirect('/admin/dash#tabs-2')

def create_size():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    print(request.form)
    new_size=Size.new(request.form['name'],request.form['description'],request.form['price'],request.form['scaling'])
    return redirect('/admin/dash#tabs-3')

def get_size(id):
    size=Size.query.get(id)
    return render_template('size.html', size = size)

def update_size(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    size=Size.query.get(id)
    size.update(request.form)
    return redirect('/admin/dash#tabs-3')

def create_order_type():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    order_type=OrderType.new(request.form['name'])
    return redirect('/admin/dash#tabs-4')

def get_order_type(id):
    order_type=OrderType.query.get(id)
    return render_template('type.html')

def update_order_type(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    order_type=OrderType.query.get(id)
    order_type.update(request.form['name'])
    return redirect('/admin/dash#tabs-4')

#admin account controller
def admin_acc():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/store')
    cur_staff=Staff.get_all()
    print(cur_staff)
    return render_template('adaccount.html', staff=cur_staff)

def create_staff():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    new_staff=Staff.new(request.form)
    return redirect('/admin/account')

#edit account
def admin_edit(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    get_staff=Staff.get(id)
    print(get_staff)
    return render_template('accedit.html',
    staff=get_staff)

def edit_user(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    staff_update = Staff.query.get(id)
    session['usr_id'] = staff_update.id
    print(staff_update.id)
    staff_update.edit_user(request.form)
    return redirect('/admin/account')

def delete_user(id):
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in_as_admin(session['employee_id'],session['login_session']):
        return redirect('/')
    staff_delete = Staff.query.get(id)
    #session['usr_id'] = staff_delete.id
    db.session.delete(staff_delete)
    db.session.commit()
    return redirect('/admin/account')

## admin nav partial
def admin_nav():
    staff_name = session['user_name']
    return render_template('adminnav.html', staff = staff_name)

### Logout routes
def admin_logout():
    session.clear()
    return redirect('/admin')

## render kitchen orders dashboard
def store():
    if not 'employee_id' in session.keys():
        return redirect('/admin')
    if not Staff.is_logged_in(session['employee_id'],session['login_session']):
        return redirect('/')
    orders=Order.get_entered()
    return  render_template('restdash.html', orders=orders)

def store_logout():
    session.clear()
    return redirect('/staff')

# Decorator to catch an event called "order_ready" (from restdash.html):
@socketio.on('order_ready', namespace='/restdash')
def handle_order_ready(message):
    # get the order id and change the status to ready
    # print("Order Ready: ",message)
    order=Order.query.get(message['order_id'])
    # print(order.id)
    order.ship_it()

@socketio.on('connect', namespace='/restdash')
def restdash_connect():
    # fires when restdash.html connects to the io socket
    print('Client connected')
