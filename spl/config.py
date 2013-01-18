# -*- coding: utf-8 -*-

from os import path

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<must be secret>'
    ASSETS_OUTPUT_DIR = 'assets'

class ProductionConfig(Config):
    MONGODB_DATABASE = 'spldata'

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'slite:///'
