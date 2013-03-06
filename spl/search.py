# -*- coding: utf-8 -*-

"""
    spl.search
    ~~~~~~~~~~

    Transform search query in json format to necessary objects to pass to
    find() method on colleciton.
"""

from pymongo import ASCENDING, DESCENDING


class OrderBy(object):
    """Represent a "sort" in Mongo query expression."""

    _directions_map = {
        'asc': ASCENDING,
        'desc': DESCENDING,
    }

    def __init__(self, field, direction="asc"):
        self.field = field
        self.direction = direction.lower()

    def __repr__(self):
        return '<OrderBy {}, {}>'.format(self.field, self.direction)


class Filter(object):
    """
    Represents a filter to apply to a query.

    A filter can be, for example, a comparison operator applied to a field of a
    model and a value or a comparision applied to two fields of the same
    document. Fore more information on posible filters, see :ref:`search`.
    """

    def __init__(self, fieldname, operator, argument=None, otherfield=None):
        self.fieldname = fieldname
        self.operator = operator
        self.argument = argument
        self.otherfield = otherfield

    def __repr__(self):
        return '<Filter {} {} {}>'.format(self.fieldname, self.operator,
                                          self.argument or self.otherfield)

    @staticmethod
    def from_dictionary(dictionary):
        fieldname = dictionary.get('name')
        operator = dictionary.get('op')
        argument = dictionary.get('val')
        otherfield = dictionary.get('field')
        return Filter(fieldname, opertor, argument, otherfield)

class SearchParameters(object):

    def __init__(self, filters=None, fields=None, order_by=None):
        self.spec = filters or []
        self.fields = fields or []
        self.sort = order_by or []

    def __repr__(self):
        return ('<SearchParameters spec={}, fields={}, sort={}>').format(self.spec, self.fields, self.sort)
