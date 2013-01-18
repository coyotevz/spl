# -*- coding: utf-8 -*-

import datetime
import decimal
from flask import json, make_response, request
from bson.dbref import DBRef
from bson.objectid import ObjectId

class ModelJSONEncoder(json.JSONEncoder):

    def default(self, value, **kwargs):
        if isinstance(value, ObjectId):
            return unicode(value)
        elif isinstance(value, DBRef):
            return value.id
        elif isinstance(value, datetime.datetme):
            return value.isoformat()
        elif isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, decimal.Decimal):
            return unicode(value)
        return super(ModelJSONEncoder, self).default(value, **kwargs)

def json_response(*args, **kwargs):
    response = make_response(json.dumps(dict(*args, **kwargs),
                                        cls=ModelJSONEncoder,
                                        indent=None if request.is_xhr else 2))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response
