from flask import render_template, redirect, request, session, flash
from config import db, datetime
from models import *
from staff_model import Staff

## render admin/staff login page
def admin():
    return render_template('admin.html')

## render staff dashboard
def staff():
    return  render_template('staff.html')

def staff_login():
    # print(' staff_login '*20)
    employee=Staff.validate_login(request.form)
    # print('*'*80,employee)
    if employee:
        session['employee_id']=employee.id
        session['user_name']=employee.first_name+' '+employee.last_name
        session['login_session']=Staff.get_session_key(employee.id)
        if employee.user_level<6:
            return redirect('/staff/dash')
        if employee.user_level>=6:
            return redirect('/admin/dash')
    return redirect('/staff/login')

#render admin dashboard
def admin_dash():
    if not 'employee_id' in session.keys():
        return redirect('/staff/login')
    if not Staff.is_logged_in_as_admin:
        return redirect('/')
    topping_menu=ToppingMenu.get_all()
    sizes=Size.get_all()
    styles=Style.get_all()
    return render_template('admindash.html',topping_menu=topping_menu,sizes=sizes,styles=styles)

def create_topping():
    print(request.form)
    new_topping=ToppingMenu.new(request.form['top_name'],request.form['description'],request.form['price'])
    # maybe change to Ajax partial:
    # return render_template('topping_menu_item.html',topping=new_topping)
    return redirect('/admin/dash')

def update_topping():
    print(request.form)
    topping=ToppingMenu.query.get(request.form['topping_id'])
    # todo: add code to save to db
    return "OK"

def update_topping_availability():
    print(request.form)
    return Topping.set_availability(request.form['topping_id'],request.form['availability'])

def create_style():
    print(request.form)
    new_style=Style.new(request.form['name'],request.form['description'],request.form['price'])
    return redirect('/admin/dash')

def create_size():
    print(request.form)
    new_size=Size.new(request.form['name'],request.form['description'],request.form['price'])
    return redirect('/admin/dash')

#admin account controller
def admin_acc():
    return render_template('adaccount.html')

#edit account
def admin_edit():
    return render_template('accedit.html')
    
## admin nav partial
def admin_nav():
    return render_template('adminnav.html')

### Logout routes
def admin_logout():
    session.clear()
    return redirect('/admin')

## render kitchen orders dashboard
def store():
    orders=Order.get_entered()
    return  render_template('restdash.html',orders=orders)

def store_logout():
    session.clear()
    return redirect('/staff')
