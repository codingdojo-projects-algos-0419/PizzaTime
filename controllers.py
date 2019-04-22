from flask import render_template, redirect, request, session, flash
from config import db, datetime
#from models import User

#### Controller Functions ####
## render admin/staff login page
def admin():
    return render_template('admin.html')

#render admin dashboard
def admin_dash():
    return render_template('admindash.html')

#admin account controller
def admin_acc():
    return render_template('adaccount.html')

#edit account
def admin_edit():
    return render_template('accedit.html')

## render staff dashboard
def staff():
    return  render_template('staff.html')

## render staff dashboard
def store():
    return  render_template('restdash.html')

### Customer controllers
## render index page with login and registration forms
def index():
    return render_template('index.html')

def members():
    return render_template('login.html')

## render quick order page
def quick():
    return render_template('quick.html')

## customer nav partial
def nav():
    return render_template('nav.html')

## admin nav partial
def admin_nav():
    return render_template('adminnav.html')

### Logout routes
def admin_logout():
    session.clear()
    return redirect('/admin')

def store_logout():
    session.clear()
    return redirect('/staff')

def logout():
    session.clear()
    return redirect('/')
