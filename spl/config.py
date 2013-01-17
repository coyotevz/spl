# -*- coding: utf-8 -*-

from os import path

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<must be secret>'
    ASSETS_OUTPUT_DIR = 'assets'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://nobix:nobix@localhost/spl'

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' %\
        path.join(path.abspath(path.curdir), 'development_data.db')
    SQLALCHEMY_RECORD_QUERIES = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'slite:///'
