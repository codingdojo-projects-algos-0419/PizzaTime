### ORM models for Orders, Pizza, and related db ###
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func, and_,or_
from config import *
import enum
import random

class StatusEnum(enum.Enum):
    # enum to track the current status of an order
    entering="Entering" # The customer has started creating an order, but not submitted it to the kitchen.
    entered="Entered"   # The customer has just submitted the order
    ready="Ready"       # The order is ready for the delivery or customer pickup
    canceled="Canceled" # The customer has canceled their current order.
    completed="Completed" # The customer has received their order.

class Order(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=False)
    order_type_id=db.Column(db.Integer,db.ForeignKey('order_type.id'),nullable=False)
    status=db.Column(db.Enum(StatusEnum))
    note=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    customer=db.relationship('Customer', foreign_keys=[customer_id],  backref=db.backref("orders",cascade="all,delete-orphan"))
    order_type=db.relationship('OrderType', foreign_keys=[order_type_id], backref=db.backref("orders",uselist=False,cascade="all, delete-orphan"))
    def complete(self):
        self.status=StatusEnum.completed
        db.session.commit()
    def reorder(self):
        self.status=StatusEnum.entering
        db.session.commit()
    def submit(self):
        self.status=StatusEnum.entered
        db.session.commit()
    def ship_it(self):
        self.status=StatusEnum.ready
        db.session.commit()
    def total(self):
        total=0.0
        for pizza in self.pizzas:
            pizza_price=(pizza.size.price+pizza.style.price)
            for topping in pizza.toppings:
                if pizza.size.scaling:
                    pizza_price+=topping.info.price*pizza.size.scaling
                else:
                    pizza_price+=topping.info.price
            total+=pizza_price*pizza.qty
        return round(total,2)
    @classmethod
    def copy(cls,order_id):
        # Make a deep copy of an order
        o_o=Order.query.get(order_id)
        new_order=cls(customer_id=o_o.customer_id,order_type_id=o_o.order_type_id,status=o_o.status,note=o_o.note)
        db.session.add(new_order)
        db.session.commit()
        # then need to copy pizzas and toppings.
        for pizza in o_o.pizzas:
            new_pizza=Pizza(order_id=new_order.id,style_id=pizza.style_id,size_id=pizza.size_id,qty=pizza.qty)
            db.session.add(new_pizza)
            db.session.commit()
            for topping in pizza.toppings:
                new_topping=Topping(pizza_id=new_pizza.id,toppings_menu_id=topping.toppings_menu_id)
                db.session.add(new_topping)
                db.session.commit()
        return new_order
    @classmethod
    def new(cls,customer_id,note=""):
        order_type=OrderType.query.first()
        # print('order type:',order_type.name)
        new_order=cls(customer_id=customer_id,order_type_id=order_type.id,status=StatusEnum.entering,note=note)
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
    @classmethod
    def get_entered(cls):
        # orders=cls.query.filter(or_(cls.status==StatusEnum.entered,cls.status==StatusEnum.ready)).all()
        orders=cls.query.filter(cls.status==StatusEnum.entered).all()
        return orders
    @classmethod
    def get_ready(cls):
        orders=cls.query.filter(cls.status==StatusEnum.ready).all()
        return orders
    @classmethod
    def get_entering(cls,customer_id):
        order=cls.query.filter(cls.customer_id==customer_id).filter(cls.status==StatusEnum.entering).first()
        return order
    @classmethod
    def get_completed(cls,customer_id):
        orders=cls.query.filter(cls.customer_id==customer_id).filter(or_(cls.status==StatusEnum.ready,cls.status==StatusEnum.completed)).all()
        return orders

class OrderType(db.Model):
    # This will probably just be "pickup" or "delivery":  The table will likely only contain these two records.
    __tablename__="order_type"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    def update(self, name):
        self.name=name
        db.session.commit()
    @classmethod
    def new(cls,name):
        new_type=cls(name=name)
        db.session.add(new_type)
        db.session.commit()
        return new_type
    @classmethod
    def get_by_name(cls,name):
        order=cls.query.filter(cls.name==name).first()
        return order
    @classmethod
    def get_all(cls):
        return cls.query.all()

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
    def price(self):
        total=(self.size.price+self.style.price)
        for topping in self.toppings:
            if self.size.scaling:
                total+=topping.info.price*self.size.scaling
            else:
                total+=topping.info.price
        total=total*self.qty
        return round(total,2)
    @classmethod
    def new(cls,order_id,form):
        size_id=form['size']
        style_id=form['style']
        qty=form['qty']
        if int(qty)<1:
            qty="1"
        new_pizza=cls(order_id=order_id,size_id=size_id,style_id=style_id,qty=qty)
        db.session.add(new_pizza)
        db.session.commit()
        topping_ids=request.form.getlist('topping')
        for topping_id in topping_ids:
            print("topping: ",topping_id)
            topping=Topping.new(new_pizza.id,topping_id)
        return new_pizza
    @classmethod
    def random(cls,order_id):
        size_id=random.randint(1,Size.query.count())
        style_id=random.randint(1,Style.query.count())
        qty="1"
        new_pizza=cls(order_id=order_id,size_id=size_id,style_id=style_id,qty=qty)
        db.session.add(new_pizza)
        db.session.commit()
        for i in range(1,random.randint(1,4)):
            topping_id=random.randint(1,ToppingMenu.query.count())
            print("topping: ",topping_id)
            topping=Topping.new(new_pizza.id,topping_id)
        return new_pizza
    @classmethod
    def delete(cls, id):
        pizza=cls.query.get(id)
        db.session.delete(pizza)
        db.session.commit()

class Size(db.Model):
    __tablename__="sizes"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    price=db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    scaling=db.Column(db.Float,default=1.0)
    def update(self,form):
        self.name=form['name']
        self.description=form['description']
        self.price=form['price']
        self.scaling=form['scaling']
        db.session.commit()
    @classmethod
    def new(cls,name,description,price,scaling):
        new_record=cls(name=name,description=description,price=price,scaling=scaling)
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
    def update(self,form):
        self.name=form['name']
        self.description=form['description']
        self.price=form['price']
        db.session.commit()
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
    pizza_id=db.Column(db.Integer,db.ForeignKey('pizzas.id'),primary_key=True)
    toppings_menu_id=db.Column(db.Integer,db.ForeignKey('toppings_menu.id'),primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    info=db.relationship('ToppingMenu',foreign_keys=[toppings_menu_id],uselist=False)
    pizza=db.relationship('Pizza',foreign_keys=[pizza_id],backref=db.backref("toppings",cascade="all,delete-orphan"))
    @classmethod
    def new(cls,pizza_id,toppings_menu_id):
        new_topping=cls(pizza_id=pizza_id,toppings_menu_id=toppings_menu_id)
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
    def update(self,form):
        self.name=form['name']
        self.description=form['description']
        self.price=form['price']
        db.session.commit()
    @classmethod
    def new(cls,name,description,price):
        new_record=cls(name=name,description=description,price=price,available=True)
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
    @classmethod
    def get_all_available(cls):
        return cls.query.filter(cls.available==True).all()
    @classmethod
    def set_availability(cls,id,available):
        topping=cls.query.get(id)
        topping.available=available
        db.session.commit()
        return "OK"

class OtherItem(db.Model):
    __tablename__="other_items"
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)
    other_items_menu_id=db.Column(db.Integer,db.ForeignKey('other_items_menu.id'),nullable=False)
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
