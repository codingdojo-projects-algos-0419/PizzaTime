from flask import render_template, redirect, request, session, flash,json
from config import db, datetime #, stripe_keys
from models import *
from customer_model import Customer, Address, State

# Stripe API #
# https://stripe.com/docs/testing
# https://testdriven.io/blog/adding-a-custom-stripe-checkout-to-a-flask-app/
# Visa card test number: 4242424242424242
import stripe
from flask_socketio import SocketIO


def show_checkout():
    #print(stripe_keys['publishable_key'])
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    order=Order.get_entering(customer.id)
    if len(order.pizzas)==0:
        return redirect('/create')
    return render_template('checkout.html',
    order=order,key=stripe_keys['publishable_key'])

def charge():
    # Action route handler from Stripe
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    order=Order.get_entering(customer.id)
    # Stripe token
    stripe_customer = stripe.Customer.create(
        email=customer.email,
        source=request.form['stripeToken']
    )
    # amount in cents, must be type int
    amount=int(order.total()*100)
    # Process charge with stripe token
    stripe.Charge.create(
        customer=stripe_customer.id,
        amount=amount,
        currency='usd',
        description='OrderID:'+str(order.id)
    )
    # change order status so it shows up in kitchen dashboard
    order.submit()
    # socket io sends a message to any connected browser connections
    # socketio.emit('neworder',order.id, namespace='/restdash')
    socketio.emit('neworder',render_template('restpartial.html',order=order),namespace='/restdash')
    # show a response to the user.
    return render_template('charge.html', amount=amount,order=order)

### Customer controllers
## render index page with login and registration forms
def index():
    return render_template('index.html')

def show_registration():
    return render_template('register.html')

def do_registration():
    #validate new user data, create new user, redirect to ordering page
    # print (request.form)
    errors=Customer.validate_info(request.form)
    print(errors)
    for error in errors:
        flash(error)
    if len(errors)==0:
        customer=Customer.new(request.form)
        session['MyWebsite_customer_id']=customer.id
        session['name']=customer.name
        session['login_session']=Customer.get_session_key(customer.id)
        return redirect ('/quick')
    return redirect ('/user/register')

def show_login():
    return render_template('login.html')

def do_login():
    #validate login credentials, redirect to ordering page
    customer=Customer.validate_login(request.form)
    if customer:
        session['MyWebsite_customer_id']=customer.id
        session['name']=customer.name
        session['login_session']=Customer.get_session_key(customer.id)
        return redirect('/quick')
    flash('Email or Password is incorrect.')
    return redirect('/user/login')

## render quick order page
def quick():
    name = session['name']
    userid = session['MyWebsite_customer_id']
    print(name)
    customer=Customer.get(userid)
    if customer.favorite_order_id:
        favorite_order=Order.query.get(customer.favorite_order_id)
    else:
        favorite_order=None
    return render_template('quick.html',
    name = name,
    userid = userid,
    order=favorite_order
    )

def show_custompizza():
    # print('customer id',session['MyWebsite_customer_id'])
    customer_id=session['MyWebsite_customer_id']
    # print('customer id',customer_id)
    customer=Customer.get(customer_id)
    # print(customer)
    order = Order.get_entering(customer.id)
    if not order:
        order=Order.new(customer_id)
        #new_pizza=Pizza.new(order.id,request.form)
    #print(order)
    sizes=Size.get_all()
    # print(sizes)
    styles=Style.get_all()
    order_types=OrderType.get_all()
    # print("order types:",order_types)
    toppings_menu=ToppingMenu.get_all()
    print(order.pizzas)
    return render_template('custompizza.html',
    sizes=sizes,
    styles=styles,
    toppings_menu=toppings_menu,
    order_types=order_types,
    order=order
    )
    # return render_template('custompizza.html')

def reorder_favorite():
    customer_id=session['MyWebsite_customer_id']
    # in case the customer has an order already started, we're going to delete it and replace it.
    customer=Customer.get(customer_id)
    fav_order=Order.query.get(customer.favorite_order_id)
    order=Order.get_entering(customer_id)
    print(order)
    if order:
        if order!=fav_order:
            Order.delete(order)
    if fav_order:
        fav_order.reorder()
    return redirect('/create')

def make_favorite():
    #this to respond to AJAX call from checkout page, or charge page
    print("Make Favorite")
    print("Fav_Order",request.form['json'])
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    py_data=json.loads(request.form['json'])
    customer.update_favorite(py_data['order_id'])
    return "ok"

## customer nav partial
def nav():
    cust_name = Customer.query.get(session['MyWebsite_customer_id'])
    name = cust_name.name
    return render_template('nav.html',
    name = name
    )

def add_pizza():
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    print("add pizza form:",request.form)
    order=Order.get_entering(customer.id)
    if not order:
        order=Order.new(customer_id)
    new_pizza=Pizza.new(order.id,request.form)
    # return redirect('/create')
    return render_template('line_order.html',pizza=new_pizza)

def random_pizza():
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    order=Order.get_entering(customer.id)
    if not order:
        order=Order.new(customer_id)
    new_pizza=Pizza.random(order.id)
    return redirect('/create')

#render account page
def cust_account():
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    cust_address=customer.addresses[0]
    print('*'*90)
    print(customer_id)
    #Get past orders
    orders=Order.get_completed(customer.id)
    print("Account Orders",orders)
    return render_template('account.html',
    customer = customer,
    orders = orders,
    address = cust_address
    )

#update customer account
def cust_update():
    update = Customer.edit_user(request.form)
    return redirect('/account')

#delete pizza order
def start_over(id):
    order=Order.get_entering(id)
    db.session.delete(order)
    db.session.commit()
    return redirect('/create')

def logout():
    session.clear()
    return redirect('/')

def delete_pizza():
    py_data=json.loads(request.form['json'])
    print("delete pizza:", py_data['pizza_id'])
    Pizza.delete(py_data['pizza_id'])
    return "ok"

def clear_order():
    py_data=json.loads(request.form['json'])
    order=Order.query.get(py_data['order_id'])
    for pizza in order.pizzas:
        Pizza.delete(pizza.id)
    return "ok"

def get_order_total():
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    order=Order.get_entering(customer.id)
    return str(order.total())
