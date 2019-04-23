from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from config import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')

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