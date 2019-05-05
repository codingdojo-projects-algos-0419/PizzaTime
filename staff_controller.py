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
    if not Staff.is_logged_in_as_admin:
        return redirect('/')
    topping_menu=ToppingMenu.get_all()
    sizes=Size.get_all()
    styles=Style.get_all()
    order_types=OrderType.get_all()
    return render_template('admindash.html',topping_menu=topping_menu,sizes=sizes,styles=styles, order_types=order_types)

def create_topping():
    print(request.form)
    new_topping=ToppingMenu.new(request.form['top_name'],request.form['description'],request.form['price'])
    # maybe change to Ajax partial:
    # return render_template('topping_menu_item.html',topping=new_topping)
    return redirect('/admin/dash')

def update_topping():
    print(request.form)
    topping=ToppingMenu.query.get(request.form['topping_id'])
    topping.update(request.form)
    return "OK"

def update_topping_availability():
    print(request.form)
    return Topping.set_availability(request.form['topping_id'],request.form['availability'])

def create_style():
    print(request.form)
    new_style=Style.new(request.form['name'],request.form['description'],request.form['price'])
    return redirect('/admin/dash')

def update_style():
    style=Style.query.get(request.form['style_id'])
    style.update(request.form)
    return redirect('/admin/dash')

def create_size():
    print(request.form)
    new_size=Size.new(request.form['name'],request.form['description'],request.form['price'])
    return redirect('/admin/dash')

def update_size():
    size=Size.query.get(request.form['size_id'])
    size.update(request.form)
    return redirect('/admin/dash')

def create_order_type():
    order_type=OrderType.new(request.form['name'])
    return redirect('/admin/dash')

def update_order_type():
    order_type=OrderType.query.get(request.form['order_type_id'])
    order_type.update(request.form['name'])
    return redirect('/admin/dash')

#admin account controller
def admin_acc():
    cur_staff=Staff.get_all()
    print(cur_staff)
    return render_template('adaccount.html', staff=cur_staff)

def create_staff():
    new_staff=Staff.new(request.form)
    return redirect('/admin/account')

#edit account
def admin_edit(id):
    get_staff=Staff.get(id)
    print(get_staff)
    return render_template('accedit.html',
    staff=get_staff)

def edit_user(id):
    staff_update = Staff.query.get(id)
    session['usr_id'] = staff_update.id
    print(staff_update.id)
    staff_update.edit_user(request.form)
    return redirect('/admin/account')

def delete_user(id):
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