from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from config import *
import enum

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')


### Model db ### 
class Customer(db.Model):
    __tablename__="customers"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(255))
    email=db.Column(db.String(255))
    phone_number=db.Column(db.String(20))
    password=db.Column(db.String(255))
    favorite_order_id=db.Column(db.Integer)
    note=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    def update_name(self,new_name):
        self.name=new_name
        db.session.commit()
    def update_email(self,new_email):
        self.email=new_email
        db.session.commit()
    def update_phone(self,new_phone):
        self.phone_number=new_phone
        db.session.commit()
    def update_password(self,new_password):
        hashed_pwd=bcrypt.generate_password_hash(new_password)
        self.password=hashed_pwd
        db.session.commit()
    def update_note(self,new_note):
        self.note=new_note
        db.session.commit()
    @classmethod
    def validate_username(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_password(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_name(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_email(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_phone(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_info(cls,customer_info):
        errors=[]
        return errors
    @classmethod
    def new(cls,customer_info):
        '''
        customer_info=[username':string,'password':string, 'name':string,'email':string,'phone':string]
        '''
        hashed_pwd=bcrypt.generate_password_hash(customer_info['password'])
        new_customer=cls(username=customer_info['username'],password=hashed_pwd,name=customer_info['name'], email=customer_info['email'],phone_number=customer_info['phone'])
        db.session.add(new_customer)
        db.session.commit()
        return new_customer
    @classmethod
    def get(cls,customer_id):
        return cls.query.get(customer_id)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def validate_login(cls,form):
        user=cls.query.filter_by(email=form['email_address']).first()
        print(user)
        if user:
            if bcrypt.check_password_hash(user.password,form['password']):
                return user
        return None
    @classmethod
    def is_logged_in(cls,user_id,login_session):
        user=cls.query.get(user_id)
        result=False
        if user:
            if bcrypt.check_password_hash(login_session,str(user.created_at)):
                result=True
        return result


class StatusEnum(enum.Enum):
    # enum to track the current status of an order
    entering="Entering" # The customer has started creating an order, but not submitted it to the kitchen.
    entered="Entered"   # The customer has just submitted the order
    ready="Ready"       # The order is ready for the delivery or customer pickup
    canceled="Canceled" # The customer has canceled their current order.

class Order(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=False)
    order_type_id=db.Column(db.Integer)
    status=db.Column(db.Enum(StatusEnum))
    note=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    customer=db.relationship('Customer', foreign_keys=[customer_id],  backref=db.backref("orders",cascade="all,delete-orphan"))
    order_type=db.relationship('OrderType', foreign_keys=[order_type_id], backref=db.backref("orders",uselist=False,cascade="all, delete-orphan"))
    @classmethod
    def new(cls,customer_id,order_type,note):
        new_order=cls(customer_id=cusomer_id,order_type_id=order_type.id,note=note)
        db.session.add(new_order)
        db.session.commit()
        return new_order
    @classmethod
    def order_count(cls):
        orders=cls.query.filter(cls.status==StatusEnum.entered).all()
        return orders
    @classmethod
    def delete(cls, order):
        db.session.delete(order)
        db.session.commit()

class OrderType(db.Model):
    # This will probably just be "pickup" or "delivery":  The table will likely only contain these two records.
    __tablename__="order_type"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    @classmethod
    def new(cls,name):
        new_type=cls(name=name)
        db.session.add(new_type)
        db.commit()
        return new_type
    @classmethod
    def get_by_name(cls,name):
        order=cls.query.filter(cls.name==name).first()
        return order

class Pizza(db.Model):
    __tablename__="pizzas"
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)
    style_id=db.Column(db.Integer,db.ForeignKey('styles.id'),nullable=False)
    size_id=db.Column(db.Integer,db.ForeignKey('sizes.id'),nullable=False)
    qty=db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    order=db.relationship('Order',foreign_keys=[order_id],backref=db.backref("pizzas",cascade="all,delete-orphan"))
    style=db.relationship('Style',foreign_keys=[style_id],backref=db.backref("pizzas"),uselist=False)
    size=db.relationship('Size',foreign_keys=[size_id],backref=db.backref("pizzas"),uselist=False)
    @classmethod
    def new(cls,order_id,size_id,style_id,qty=1):
        new_pizza=cls(order=order_id,size_id=size_id,style_id=style_id,qty=qty)
        db.session.add(new_pizza)
        db.session.commit()
        return new_pizza

class Size(db.Model):
    __tablename__="sizes"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    price=db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    @classmethod
    def new(cls,name,description,price):
        new_record=cls(name=name,description=description,price=price)
        db.session.add(new_record)
        db.session.commit()
        return new_record
    @classmethod
    def get_by_name(cls,name):
        record=cls.query.filter(cls.name==name).first()
        return record
    @classmethod
    def get_all(cls):
        return cls.query.all()

class Style(db.Model):
    __tablename__="styles"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    price=db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    @classmethod
    def new(cls,name,description,price):
        new_record=cls(name=name,description=description,price=price)
        db.session.add(new_record)
        db.session.commit()
        return new_record
    @classmethod
    def get_by_name(cls,name):
        record=cls.query.filter(cls.name==name).first()
        return record
    @classmethod
    def get_all(cls):
        return cls.query.all()

class Topping(db.Model):
    __tablename__="toppings"
    pizza_id=db.Column(db.Integer,primary_key=True)
    toppings_menu_id=db.Column(db.Integer,primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    info=db.relationship('ToppingMenu',foreign_keys=[toppings_menu_id],uselist=False)
    pizza=db.relationship('Pizza',foreign_keys=[pizza_id],backref=db.backref("toppings",cascade="all,delete-orphan"))
    @classmethod
    def new(cls,pizza_id,toppings_menu_id):
        new_topping=cls(pizza_id=pizz_id,toppings_menu_id=toppings_menu_id)
        db.session.add(new_topping)
        db.session.commit()

class ToppingMenu(db.Model):
    __tablename__="toppings_menu"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    price=db.Column(db.Float)
    available=db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    @classmethod
    def new(cls,name,description,price):
        new_record=cls(name=name,description=description,price=price)
        db.session.add(new_record)
        db.session.commit()
        return new_record
    @classmethod
    def get_by_name(cls,name):
        record=cls.query.filter(cls.name==name).first()
        return record
    @classmethod
    def get_all(cls):
        return cls.query.all()

class OtherItem(db.Model):
    __tablename__="other_items"
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)
    other_items_menu_id=db.Column(db.Integer,db.ForeignKey('other_items_menus.id'),nullable=False)
    qty=db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    order=db.relationship('Order',foreign_keys=[order_id],backref=db.backref("other_items",cascade="all,delete-orphan"))
    info=db.relationship('OtherItemsMenu',foreign_keys=[other_items_menu_id],uselist=False)
    @classmethod
    def new(cls,order_id,other_items_menu_id,qty=1):
        new_item=cls(order_id=order_id,other_items_menu_id=other_items_menu_id,qty=qty)
        db.session.add(new_item)
        db.session.commit()

class OtherItemsMenu(db.Model):
    __tablename__="other_items_menu"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    price=db.Column(db.Float)
    available=db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    @classmethod
    def new(cls,name,description,price):
        new_record=cls(name=name,description=description,price=price)
        db.session.add(new_record)
        db.session.commit()
        return new_record
    @classmethod
    def get_all(cls):
        return cls.query.all()

class Address(db.Model):
    __tablename__="addresses"
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=False)
    street_address=db.Column(db.String(255))
    city=db.Column(db.String(255))
    state_id=db.Column(db.Integer,db.ForeignKey('states.id'),nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    state=db.relationship('State',foreign_keys=[state_id],uselist=False)
    customer=db.relationship('Customer',foreign_keys=[customer_id],backref=db.backref("addresses",cascade="all,delete-orphan"))
    @classmethod
    def new(cls,address):
        new_address=cls(customer_id=address['customer_id'],street_address=address['street_address'],city=address['city'],state_id=address['city'])
        db.session.add(new_address)
        db.session.commit()
    

class State(db.Model):
    __tablename__="states"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(2))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    @classmethod
    def add(cls,name):
        state=cls(name=name)
        db.session.add(state)
        db.session.commit()
    @classmethod
    def get_all(cls):
        return cls.query.all()

class Staff(db.Model):
    __tablename__="staff"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255))
    email=db.Column(db.String(255))
    first_name=db.Column(db.String(255))
    last_name=db.Column(db.String(255))
    user_level=db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    def update_username(self,new_username):
        self.username=new_username
        db.session.commit()
    def update_first(self,new_fname):
        self.first_name=new_fname
        db.session.commit()
    def update_last(self,new_lname):
        self.last_name=new_lname
        db.session.commit()
    def update_email(self,new_email):
        self.email=new_email
        db.session.commit()
    def update_password(self,new_password):
        hashed_pwd=bcrypt.generate_password_hash(new_password)
        self.password=hashed_pwd
        db.session.commit()
    def make_admin(self):
        self.user_level=10
        db.session.commit()
    def make_staff(self):
        self.user_level=0
        db.session.commit()
    @classmethod
    def validate_username(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_password(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_email(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_phone(cls,name):
        errors=[]
        return errors
    @classmethod
    def validate_info(cls,customer_info):
        errors=[]
        return errors
    @classmethod
    def new(cls,customer_info):
        '''
        customer_info=[username':string,'password':string, 'name':string,'email':string,'phone':string]
        '''
        hashed_pwd=bcrypt.generate_password_hash(customer_info['password'])
        new_customer=cls(username=customer_info['username'],password=hashed_pwd,name=customer_info['name'], email=customer_info['email'],phone_number=customer_info['phone'])
        db.session.add(new_customer)
        db.session.commit()
        return new_customer
    @classmethod
    def get(cls,customer_id):
        return cls.query.get(customer_id)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_all_staff(cls):
        return cls.query.filter(cls.user_level<6).all()
    def get_all_admins(cls):
        return cls.query.filter(cls.user_level>=6).all()
    @classmethod
    def get_session_key(cls,user_id):
        user=cls.query.get(user_id)
        session_key=bcrypt.generate_password_hash(str(user.created_at))
        return session_key
    @classmethod
    def validate_login(cls,form):
        user=cls.query.filter_by(email=form['email_address']).first()
        print(user)
        if user:
            if bcrypt.check_password_hash(user.password,form['password']):
                return user
        return None
    @classmethod
    def is_logged_in(cls,user_id,login_session):
        user=cls.query.get(user_id)
        result=False
        if user:
            if bcrypt.check_password_hash(login_session,str(user.created_at)):
                result=True
        return result
    @classmethod
    def is_logged_in_as_admin(cls,admin_id,login_session):
        user=cls.query.get(admin_id)
        result=False
        if user:
            if bcrypt.check_password_hash(login_session,str(user.created_at)):
                if user.user_level==9:
                    print("admin login_success")
                    result=True
        return result