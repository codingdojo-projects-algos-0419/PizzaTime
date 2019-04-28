from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from config import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
PHONE_REGEX=re.compile('^\d{3}-\d{3}-\d{4}$')

class Customer(db.Model):
    __tablename__="customers"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255))
    name=db.Column(db.String(255))
    email=db.Column(db.String(255),nullable=False)
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
    def validate_username(cls,username):
        errors=[]
        existing_users=cls.query.filter(cls.username==username).count()
        if (existing_users)>0:
            errors.append("This user's first and last name is already registered!")
        return errors
    @classmethod
    def validate_password(cls, password, confirm_password):
        errors=[]
        if len(password)<5:
            errors.append("Password must be at least 5 characters long!")
        if password!=confirm_password:
            errors.append("Passwords don't match!")
        return errors
    @classmethod
    def validate_name(cls,name):
        errors=[]
        if len(name)<3:
            errors.append("Please enter your name (at leat 3 characters).")
        # if not name.isalpha():
        #     errors.append("Names must be alphabet characters only!")
        return errors
    @classmethod
    def validate_email(cls,email_address):
        errors=[]
        if not EMAIL_REGEX.match(email_address):    # test whether a field matches the pattern
            errors.append("Invalid email address!")
        existing_users=cls.query.filter_by(email=email_address).count()
        if (existing_users)>0:
            errors.append("This email address is currently in use by another user!")
        return errors
    @classmethod
    def validate_phone(cls,phone_number):
        errors=[]
        if len(phone_number)<7:
            errors.append("Please enter a valid 10 digit phone number.")
        # if not PHONE_REGEX.match(phone_number):
        #     errors.append("Please enter a valid phone number.")
        return errors
    @classmethod
    def validate_info(cls,customer_info):
        errors=[]
        #errors+=validate_username(customer_info['username'])
        errors+=cls.validate_name(customer_info['name'])
        errors+=cls.validate_password(customer_info['password'],customer_info['confirm_password'])
        errors+=cls.validate_email(customer_info['email_address'])
        errors+=cls.validate_phone(customer_info['phone_number'])
        return errors
    @classmethod
    def new(cls,customer_info):
        '''
        customer_info=[username':string,'password':string, 'name':string,'email':string,'phone':string]
        '''
        hashed_pwd=bcrypt.generate_password_hash(customer_info['password'])
        # new_customer=cls(username=customer_info['username'],password=hashed_pwd,name=customer_info['name'], email=customer_info['email'],phone_number=customer_info['phone'])
        new_customer=cls(username=customer_info['email_address'],password=hashed_pwd,name=customer_info['name'], email=customer_info['email_address'],phone_number=customer_info['phone_number'])
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
    @classmethod
    def get_session_key(cls,id):
        user=cls.query.get(id)
        session_key=bcrypt.generate_password_hash(str(user.created_at))
        return session_key

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
    def new(cls,name):
        state=cls(name=name)
        db.session.add(state)
        db.session.commit()
    @classmethod
    def get_all(cls):
        return cls.query.all()
