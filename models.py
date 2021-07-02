import os
from datetime import datetime
from peewee import *
from flask_login import UserMixin
import boto3

database_name = 'pupr'

s3 = boto3.resource('s3')

DATABASE = PostgresqlDatabase(database_name)

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Dog(Model):
    name = CharField()
    owner = ForeignKeyField(User, backref=database_name)
    photos = CharField()
    description = CharField()
    created_timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE

class Likes(Model):
    dog = ForeignKeyField(Dog, backref=database_name)
    did_like_dog = BooleanField()
    like_sending_user = ForeignKeyField(User, backref=database_name)
    created_timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, User, Likes], safe=True)
    print("TABLES Created")
    DATABASE.close()