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

    /suppliers/                 GET         - Gives a list of all suppliers (paginated)
    /suppliers/                 POST        - Create a new supplier
    /suppliers/<supplier_id>    GET         - Returns a specified supplier
    /suppliers/<supplier_id>    PUT         - Updates a specified supplier
    /suppliers/<supplier_id>    DELETE      - Delete a specified supplier
    """
    def get(self, supplier_id):
        if supplier_id is None:
            p = Pagination(db.Supplier.find().sort('name'), page=request.page,
                           per_page=request.per_page)
            data = {
                'objects': p.items,
                'page': p.page,
                'num_results': p.total,
                'num_pages': p.pages,
            }
        else:
            data = db.Supplier.get_or_404(supplier_id)
        import time; time.sleep(1)
        return json_response(data)


register_api(SupplierAPI, 'supplier_api', '/suppliers/', pk='supplier_id', pk_type='ObjectId')


class ContactAPI(MethodView):
    """
    Contacts API definition
    ~~~~~~~~~~~~~~~~~~~~~~~

    /contacts/                  GET         - Gives a list of all contacts (paginated)
    /contacts/                  POST        - Create a new contact
    /contacts/<contact_id>      GET         - Returns a specified contact
    /contacts/<contact_id>      PUT         - Updates a specified contact
    /contacts/<contact_id>      DELETE      - Delete a specified contact
    """
    def get(self, contact_id):
        if contact_id is None:
            p = Pagination(db.Contacts.find().sort('name'), page=request.page,
                           per_page=request.per_page)
            data = {
                'objects': p.items,
                'page': p.page,
                'num_results': p.total,
                'num_pages': p.pages,
            }
        else:
            data = db.Contacts.get_or_404(contact_id)
        import time; time.sleep(1)
        return json_response(data)

register_api(ContactAPI, 'contact_api', '/contacts/', pk='contact_id', pk_type='ObjectId')


def configure_api(app):
    app.register_blueprint(api)
