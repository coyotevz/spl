# -*- coding: utf-8 -*-

import os
from os import path
import locale

locale.setlocale(locale.LC_ALL, '')

from flask import Flask
from spl.models import configure_db
from spl.views import configure_views
from spl.api import configure_api
from spl.jinjafilters import configure_jinjafilters

DEFAULT_APPNAME = 'spl'

def create_app(app_name=None, config=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name)

    configure_app(app, config)
    configure_db(app)
    configure_views(app)
    configure_api(app)
    configure_jinjafilters(app)

    return app


def configure_app(app, config=None):

    app.config.from_object('spl.config.DevelopmentConfig')
    #app.logger.info("Config: Development")

    if config is not None:
        app.config.from_object(config)

    @app.route('/')
    def index():
        from flask import escape
        return '<pre>'+str(escape(str(app.url_map)))+'</pre>'