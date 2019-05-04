from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import datetime
import re
import stripe

app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)
app.secret_key="secret#key#is#set"
bcrypt = Bcrypt(app)

# Stripe API #
# Strip API keys go in a folder above called StripeAPIkeys.txt
#f = open("..\StripeAPIkeys.txt", "r")
#stripe_keys = {
#'publishable_key':f.readline().strip('\n').strip('\r'),
#'secret_key': f.readline().strip('\n').strip('\r')
#}
#f.close()
#stripe.api_key = stripe_keys['secret_key']

#print("Public key",stripe_keys['publishable_key'])
#print("Secret key",stripe_keys['secret_key'])
