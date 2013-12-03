# -*- coding: utf-8 -*-

import os
from os import path
import locale

locale.setlocale(locale.LC_ALL, '')

from flask import Flask, request
from spl.models import configure_db
from spl.views import configure_views
from spl.api import configure_api
from spl.jinjafilters import configure_jinjafilters
from spl.assets import configure_bundles

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
    configure_bundles(app)

    return app


def configure_app(app, config=None):

    app.config.from_object('spl.config.DevelopmentConfig')
    #app.logger.info("Config: Development")

    if config is not None:
        app.config.from_pyfile(config)

    @app.route('/')
    def index():
        from flask import escape
        return '<pre>'+str(escape(str(app.url_map)))+'</pre>'

    @app.route('/design/')
    def dev_design():
        from flask import render_template
        from spl.models import db
        return render_template('design.html', db=db)

    @app.route('/design2/')
    def dev_design():
        from flask import render_template
        from spl.models import db
        return render_template('design2.html', db=db)

    @app.before_request
    def before_request():
        max_per_page = app.config.get('MAX_ITEMS_PER_PAGE', 100)
        request.page = int(request.args.get('page', 1))
        request.per_page = min(int(request.args.get('per_page', 25)), max_per_page)
