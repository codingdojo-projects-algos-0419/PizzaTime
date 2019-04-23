from flask import render_template, redirect, request, session, flash
from config import db, datetime
from models import *
from customer_model import Customer, Address, State

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

def logout():
    session.clear()
    return redirect('/')
