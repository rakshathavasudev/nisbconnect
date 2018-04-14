from peewee import *
from flask_bcrypt import generate_password_hash

myDB = MySQLDatabase(host="localhost",port=3306,user="root",passwd="1234",database="codejam")

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

class User(UserMixin,BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=200)
    joined_at = DateTimeField(default=datetime.datetime.now)
    bio = TextField()
    dob = DateTimeField(default=datetime.datetime.now)
    ieee_no = CharField(unique=True)
    branch = CharField()
    sem = CharField()



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
