import os
from env import *

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ''

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = sqlpath()