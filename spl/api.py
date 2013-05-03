# -*- coding: utf-8 -*-

from flask import request
from spl.models import db
from spl.utils import json_response, Pagination

from spl.rest import ResourceView, ManagerAPI


rest = ManagerAPI('api', __name__, url_prefix='/api')


class SupplierResource(ResourceView):

    endpoint = 'supplier_api'
    url = 'suppilers'
    collection = lambda x: db.Supplier

rest.register_resource(SupplierResource)


class ContactResource(ResourceView):

    endpoint = 'contact_api'
    url = 'contacts'

    collection = lambda x: db.Contact

rest.register_resource(ContactResource)


def configure_api(app):
    rest.init_app(app)
