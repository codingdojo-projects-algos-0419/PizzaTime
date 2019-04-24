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
    return render_template('admindash.html')

def create_topping():
    pass
    
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

## render staff dashboard
def store():
    return  render_template('restdash.html')

def store_logout():
    session.clear()
    return redirect('/staff')
