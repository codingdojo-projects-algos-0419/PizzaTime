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

## render staff dashboard
def staff():
    return  render_template('staff.html')

## render staff dashboard
def store():
    return  render_template('restdash.html')

## render index page with login and registration forms
def index():
    return render_template('index.html')

def members():
    return render_template('login.html')

## render quick order page
def quick():
    return render_template('quick.html')

def nav():
    return render_template('nav.html')

def admin_logout():
    session.clear()
    redirect('/admin')

def logout():
    session.clear()
    redirect('/')
