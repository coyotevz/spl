# -*- coding: utf-8 -*-

"""
    spl.rest
    ~~~~~~~~

    Provides the  folowing view classes, subclasses of :class:`spl.rest.API`

    Provides the endpoints for each of the basic HTTP methods. This is the
    main class used by the :meth:`APIManager.create_api` method to create
    endpoints.
"""

from collections import defaultdict
from math import ceil
from bson.objectid import ObjectId

from flask import abort, current_app, request, json, Blueprint
from flask.views import MethodView

from spl.utils import json_response
from spl.search import SearchParameters


def search(collection, params):
    import pprint
    pprint.pprint(params)
    nparams = SearchParameters.from_dictionary(params)
    pprint.pprint(nparams)
    pprint.pprint(nparams.build())
    return collection.find(**nparams.build())


class AuthenticationException(Exception):
    """Raised when authentication failed for some reason.
    """
    def __init__(self, message='', status_code=401, *args, **kwargs):
        super(AuthenticationException, self).__init__(*args, **kwargs)
        self.message = message
        self.status_code = status_code


def jsonify_status_code(status_code, *args, **kwargs):
    """Returns a jsonified response with the specified HTTP status code.
    """
    response = json_response(*args, **kwargs)
    response.status_code = status_code
    return response


class ResourceView(MethodView):

    def __init__(self, *args, **kwargs):
        if callable(self.collection):
            self.collection = self.collection()

    def get(self, instid):
        """Returns a JSON representation of an instance of a document with the
        specified name.

        If ``instid`` is ``None``, this methods returns the result of a search
        with parameters specified in the query string of the request. If no
        search parameters are specified, this method returns all instances of
        the specified document.

        If ``instid`` is an integer, this method returns the instance of the
        document with that indentifying integer. If no such instances exists,
        this method respond with :http:status:`404`.
        """
        if instid is None:
            return self._get_search()
        return self._get_single(instid)

    def delete(self, instid):
        """Removes the specified instance from collection with the specified
        name from the database.

        Since :http:method:`delete` is an idempotent method according to the
        :rfc:`2616`, this method respond with :http:status:`204` regardless of
        whether an object was deleted.
        """
        is_deleted = False
        inst = self.collection.get_from_id(instid)
        if inst is not None:
            inst.delete()
            is_deleted = True
        return jsonify_status_code(204)

    def post(self):
        """Creates a new instance of a given model based on request data.

        This function parses the string contained in :attr:`flask.request.data`
        as a JSON object and then validates it with a validator specified in
        the constructor of this class.
        """
        # try to read the parameters for the model from body of the request
        try:
            params = json.loads(request.data)
        except (TypeError, ValueError, OverflowError):
            return jsonify_status_code(400, message='Unable to decode data')

        instance = self.collection(doc=params)
        instance.save()

        return jsonify_status_code(201, instance)

    def put(self, instid):
        """Updates the instance specified by ``instid`` of the named model, or
        updates multiple instance if ``instid`` is ``None``.

        The :attr:`flask.request.data` attribute will be parse a s JSON object
        containing the mapping from field name to value to which to update the
        specified instance or instances.
        """
        pass

    def patch(self, instid):
        """Alias for :meth:`put`."""
        return self.put(instid)

    # Private API

    def _get_single(self, instid):
        result = self.collection.get_from_id(instid)
        if result is None:
            abort(404)
        return json_response(result)

    def _get_search(self):
        """Defines a generic search function for the database document.

        If the query string is empty, or if the psecified query is invalid for
        some reason (for example, searching for all person instances with), the
        response will be the JSON string ``{'objects': []}``.

        To search for entities meeting some criteria, the client makes a
        request to :http:get:`/api/<collectionname>` with a query string
        containing the parameter of the search. The parameters of the search
        can involve filters.

        TODO: Continue documentation
        """
        # try to get search query from the request query parameters
        try:
            data = json.loads(request.args.get('q', '{}'))
        except (TypeError, ValueError, OverflowError):
            return jsonify_status_code(400, message='Unable to decode data')

        try:
            result = search(self.collection, data)
        except Exception as e:
            return jsonify_status_code(400, message=e.message)
            return jsonify_status_code(400,
                                       message='Unable to construct query')

        return self._paginated(result)

    def _paginated(self, cursor):
        """Returns a paginated JSONified response from the specified list of
        model instances.

        `cursor` is a cursor returned by :meth:`find` collection method.

        The response data is JSON of the form::

        .. sourcecode::javascript

           {
             'page': 2,
             'total_pages': 3,
             'num_results': 8,
             'objects': [{'_id': '...', 'name': 'Jeffrey', 'age': 24}, ...]
           }
        """
        num_results = cursor.count()
        # get the results per page form query string or config
        max_per_page = current_app.config.get('MAX_ITEMS_PER_PAGE', 100)
        per_page = min(int(request.args.get('per_page', 25)), max_per_page)
        # get the page number (first page is page 1)
        page = int(request.args.get('page', 1))
        if (page < 1) or (per_page < 1):
            abort(404)
        items = list(cursor.skip((page - 1) * per_page).limit(per_page))
        if not items and page != 1:
            abort(404)
        return json_response({
            'page': page,
            'num_results': num_results,
            'num_pages': int(ceil(num_results / float(per_page))),
            'objects': items,
        })

class ManagerAPI(Blueprint):

    def __init__(self, *args, **kwargs):
        self.app = None
        self._to_register = []
        if 'app' in kwargs:
            self.app = kwargs.pop('app')
        super(ManagerAPI, self).__init__(*args, **kwargs)

    def init_app(self, app=None):
        self.app = app if app is not None else self.app
        for res, kw in self._to_register:
            self._register(res, kw)
        self._to_register = []
        self.app.register_blueprint(self)

    def register_resource(self, resource, **kwargs):
        if self.app is None:
            self._to_register.append((resource, kwargs))
        else:
            self._register(resource, kwargs)

    def _register(self, resource, kw=None):
        if kw is None:
            kw = {}
        endpoint = _get_endpoint(resource, kw)
        url = _get_url(resource, kw)
        view_func = resource.as_view(endpoint)
        self.add_url_rule(url, defaults={'instid': None}, view_func=view_func,
                          methods=['GET',])
        self.add_url_rule(url, view_func=view_func, methods=['POST',])
        self.add_url_rule('%s<ObjectId:instid>' % (url,), view_func=view_func,
                          methods=['GET', 'PUT', 'PATCH', 'DELETE'])


def _get_endpoint(resource, params):
    return '%s' % _get_attr('endpoint', resource, params)

def _get_url(resource, params):
    url = _get_attr('url', resource, params)
    if not url.startswith('/'):
        url = '/' + url
    if not url.endswith('/'):
        url = url + '/'
    return url

def _get_attr(attr, resource, params):
    if attr in params:
        return params.get(attr)
    if hasattr(resource, attr) and getattr(resource, attr) is not None:
        return getattr(resource, attr)
    return resource.__name__.lower()
