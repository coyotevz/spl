# -*- coding: utf-8 -*-

from flask import Blueprint, request
from flask.views import MethodView
from spl.models import db
from spl.utils import json_response


api = Blueprint('api', __name__, url_prefix='/api')

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    api.add_url_rule(url, defaults={pk: None}, view_func=view_func,
                     methods=['GET', 'POST'])
    api.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


class SupplierAPI(MethodView):
    """
    Suppliers API definition
    ~~~~~~~~~~~~~~~~~~~~~~~~

    /suppliers/         GET         - Index method that returns a suppliers list
    /suppliers/         POST        - Create a new supplier
    """
    def get(self, id):
        return json_response({'objects': list(db.Supplier.find())})


register_api(SupplierAPI, 'supplier_api', '/suppliers/')


def configure_api(app):
    app.register_blueprint(api)
