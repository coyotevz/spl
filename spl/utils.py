# -*- coding: utf-8 -*-

import datetime
import decimal
from math import ceil
from flask import json, make_response, request, abort
from bson.dbref import DBRef
from bson.objectid import ObjectId

class ModelJSONEncoder(json.JSONEncoder):

    def default(self, value, **kwargs):
        if isinstance(value, ObjectId):
            return unicode(value)
        elif isinstance(value, DBRef):
            return value.id
        elif isinstance(value, datetime.datetime):
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


class Pagination(object):
    """
    Internal helper class to paginate query results.
    """

    def __init__(self, cursor, page, per_page):
        if page < 1:
            abort(404)
        #: the unlimited cursor object that was used to create this
        #: pagination object.
        self.cursor = cursor
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the cursor
        self.total = cursor.count()
        #: the items for the current page
        items = list(cursor.clone().skip((page - 1) * per_page).limit(per_page))
        if not items and page != 1:
            abort(404)
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        return int(ceil(self.total / float(self.per_page)))

    def prev(self):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.cursor is not None, 'a cursor object is required'
        return Pagination(self.cursor, self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Return number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    def next(self):
        assert self.cursor is not None, 'a cursor object is required'
        return Pagination(self.cursor, self.page + 1, self.per_page)

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(elf):
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """
        Iterates over the page numbers in the pagination.  The four parameters
        control the threshold how many numbers should be produced for the
        sides.  Skipped page numbers are represented as `None`.  This is how
        you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                    if last + 1 != num:
                       yield None
                    yield num
                    last = num
