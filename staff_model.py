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
    password=db.Column(db.String(255))
    email=db.Column(db.String(255))
    first_name=db.Column(db.String(255))
    last_name=db.Column(db.String(255))
    user_level=db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr(self):
        return '<Staff{}>'.format(self.username)
    def __repr(self):
        return '<Staff{}>'.format(self.first_name)

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
    def create_default_admin(cls):
        '''
        Create a default administrator to start the database with.
        Normally you would call this only from a command line python session.
        '''
        staff_info={'username': 'admin', 'first_name': 'default', 'last_name': 'admin', 'password': 'changeme', 'email':''}
        admin=cls.new(staff_info)
        admin.make_admin()
        return admin
    @classmethod
    def new(cls,staff_info):
        '''
        staff_info=[username':string,'password':string, 'first_name':string,'last_name':string; 'email':string]
        run Staff.validate_info(staff_info) before calling this method
        '''
        hashed_pwd=bcrypt.generate_password_hash(staff_info['password'])
        new_staff=cls(username=staff_info['username'],password=hashed_pwd,first_name=staff_info['first_name'],last_name=staff_info['last_name'], email=staff_info['email'],user_level=0)
        db.session.add(new_staff)
        db.session.commit()
        return new_staff
    @classmethod
    def delete(cls,staffer_id):
        staffer=cls.query.get(staffer_id)
        db.session.delete(staffer)
        db.session.commit()
    @classmethod
    def get(cls,staffer_id):
        return cls.query.get(staffer_id)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_all_staff(cls):
        return cls.query.filter(cls.user_level<6).all()
    @classmethod
    def get_all_admins(cls):
        return cls.query.filter(cls.user_level>=6).all()
    @classmethod
    def get_session_key(cls,staffer_id):
        user=cls.query.get(staffer_id)
        session_key=bcrypt.generate_password_hash(str(user.created_at))
        return session_key
    @classmethod
    def validate_login(cls,form):
        '''
        form=['username':string,'password':string]
        '''
        # print(form)
        user=cls.query.filter(cls.username==form['username']).first()
        # print('*'*80,user)
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

    @classmethod
    def edit_user(cls,form):
        staff_update = Staff.query.get(session['usr_id'])
        staff_update.first_name = form['first_name']
        staff_update.last_name = form['last_name']
        staff_update.username = form['username']
        staff_update.email = form['email']
        staff_update.user_level = form['user_level']
        db.session.commit()
        return staff_update.first_name
