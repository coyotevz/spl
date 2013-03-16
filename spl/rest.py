# -*- coding: utf-8 -*-

"""
    spl.rest
    ~~~~~~~~

    Provides the  folowing view classes, subclasses of :class:`spl.rest.API`

    Provides the endpoints for each of the basic HTTP methods. This is the
    main class used by the :meth:`APIManager.create_api` method to create
    endpoints.
"""

from math import ceil
from bson.objectid import ObjectId

from flask import abort, current_app, request, json
from flask.views import MethodView

from spl.utils import json_response
from spl.search import SearchParameters


def search(collection, params):
    nparams = SearchParameters.from_dictionary(params)
    print nparams.build()
    return collection.find(**params)


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


class API(MethodView):

    def __init__(self, *args, **kwargs):
        if callable(self.collection):
            self.collection = self.collection()

    def _check_authentication(self):
        """Raises an exception if the current user is not authorized to make a
        request.

        If the specified HTTP method requries authentication (see the
        constructor), this function calls the authentication function specified
        by the ``authentication_function`` keyword argument to the constructor
        of this class. That functon my raise :exc:`AuthenticationException` if
        the current suer is not authorized to make the request.
        """
        if request.method in self.authentication_required_for:
            self.authentication_function()

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

    def _search(self):
        """Defines a generic search function for the database document.

        If the query string is empty, or if the psecified query is invalid for
        some reason (for example, searching for all person instances with), the
        response will be the JSON strnig ``{'objects': []}``.

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

    def _get_by(self, primary_key):
        return self.collection.find_one(ObjectId(primary_key))

    def _inst(self, instid):
        inst = self._get_by(instid)
        if inst is None:
            abort(404)
        return inst

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
        try:
            self._check_authentication()
        except AuthenticationException, e:
            return jsonify_status_code(status_code=e.status_code,
                                       message=e.message)

        if instid is None:
            return self._search()

        return self._inst(instid)

    def delete(self, instid):
        """Removes the specified instance from collection with the specified
        name from the database.

        Since :http:method:`delete` is an idempotent method according to the
        :rfc:`2616`, this method respond with :http:status:`204` regardless of
        whether an object was deleted.
        """
        pass

    def post(self):
        """Creates a new instance of a given model based on request data.

        This function parses the string contained in :attr:`flask.request.data`
        as a JSON object and then validates it with a validator specified in
        the constructor of this class.
        """
        pass

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
