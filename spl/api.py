# -*- coding: utf-8 -*-

from flask import Blueprint, request
from flask.views import MethodView
from spl.models import db
from spl.utils import json_response, Pagination


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
        p = Pagination(db.Supplier.find(), page=request.page,
                       per_page=request.per_page)
        return json_response({
            'objects': p.items,
            'page': p.page,
            'num_results': p.total,
            'num_pages': p.pages,
        })


register_api(SupplierAPI, 'supplier_api', '/suppliers/')


def configure_api(app):
    app.register_blueprint(api)
