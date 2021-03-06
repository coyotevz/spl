# -*- coding: utf-8 -*-

"""
    spl.search
    ~~~~~~~~~~

    Transform search query in json format to necessary objects to pass to
    find() method on colleciton.
"""

from pymongo import ASCENDING, DESCENDING


INCLUDE = 1
EXCLUDE = 0


def _mk_std_selector(s):
    def sel(field, arg):
        return {field: {'$' + s: arg}}
    sel.__name__ = '_' + s
    return sel

_selectors = ['ne', 'gt', 'gte', 'lt', 'lte', 'in', 'nin']

OPERATORS = {
    'eq': lambda f, a: {f: a},
}

OPERATORS.update([(s, _mk_std_selector(s)) for s in _selectors])

OPERATORS.update({
    'like': lambda f, a: {f: {'$regex': a}},
    'ilike': lambda f, a: {f: {'$regex': a, '$options': 'i'}},
    'endswith': lambda f, a: {f: {'$regex': a + '$'}},
    'startswith': lambda f, a: {f: {'$regex': '^' + a}},
    'contains': lambda f, a: {f: {'$regex': a}},
    'icontains': lambda f, a: {f: {'$regex': a, '$options': 'i'}},
})

_alias = {
    '==': 'eq',
    'equals': 'eq',
    'equal_to': 'eq',
    '!=': 'ne',
    'neq': 'ne',
    'not_equal_to': 'ne',
    'does_not_equal': 'ne',
    '>': 'gt',
    '<': 'lt',
    '>=': 'gte',
    '<=': 'lte',
    'not_in': 'nin',
}

def to_list(l):
    if not l:
        return list()
    return list([l])


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

    def build(self):
        return (self.field, self._directions_map[self.direction])


class Filter(object):
    """
    Represents a filter to apply to a query.

    A filter can be, for example, a comparison operator applied to a field of a
    document and a value or a comparision applied to two fields of the same
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
        """
        Returns a new :class:`Filter` object with arguments parsed from
        `dictionary`.

        where ``dictionary['name']`` is the name of the field of the document
        on which to apply the operator, ``dictionary['op']`` is the name of the
        operator to apply, ``dictionary['val']`` is the value on the right to
        which the operator will be applied, and ``dictionary['other']`` is the
        name of the other field of the document to which the operator will be
        applied.
        `dictionary` is a dictionary of the form::

            {'name': 'age', 'op': 'lt', 'val': 20}

        or::

            {'name': 'age', 'op': 'lt', 'other': 'height'}

        where ``dictionary['name']`` is the name of the field of the document
        on which to apply the operator, ``dictionary['op']`` is the name of the
        operator to apply, ``dictionary['val']`` is the value on the right to
        which the operator will be applied, and ``dictionary['other']`` is the
        name of the other field of the document to which the operator will be
        applied.
        """
        fieldname = dictionary.get('name')
        operator = dictionary.get('op')
        argument = dictionary.get('val')
        otherfield = dictionary.get('field')
        return Filter(fieldname, operator, argument, otherfield)

    def build(self):
        if self.operator in OPERATORS:
            op = OPERATORS[self.operator]
        elif self.operator in _alias:
            op = OPERATORS[_alias[self.operator]]
        else:
            raise KeyError('Operator "{}" does not exists'.format(self.operator))

        return op(self.fieldname, self.argument or self.otherfield)


class Fields(object):

    def __init__(self, data):
        if isinstance(data, dict):
            inc = data.get('include', [])
            exc = data.get('exclude', [])
        elif isinstance(data, list):
            exc = [s[1:] for s in data if s.startswith('-')]
            inc = [s for s in data if s[1:] not in exc]
        else:
            inc = exc = []
        self.include = inc
        self.exclude = exc

    def __repr__(self):
        return '<Fields include={}, exclude={}>'.format(self.include, self.exclude)

    def __nonzero__(self):
        return bool(self.include) or bool(self.exclude)

    def build(self):
        return dict(
            [(f, INCLUDE) for f in self.include] or
            [(f, EXCLUDE) for f in self.exclude]
        )


class SearchParameters(object):

    def __init__(self, filters=None, fields=None, order_by=None):
        self.spec = filters or []
        self.fields = fields or []
        self.sort = order_by or []

    def __repr__(self):
        return ('<SearchParameters spec={}, fields={}, sort={}>').format(self.spec, self.fields, self.sort)

    @staticmethod
    def from_dictionary(dictionary):
        """
        Returns a new :class:`SearchParameters` object with arguments parsed
        from `dictionary`.

        `dictionary` is a dictionary of the form::

            {
              'filters': [{'name': 'age', 'op': 'lt', 'val': 20}, ...],
              'order_by': [{'field': 'age', 'direction': 'desc'], ...],
              'fields': {'include': ['age', '_id'], 'exclude': ['address']},
            }

        The provided dictionary may have other key/value pairs, but they are
        ignored.
        """
        fd = Filter.from_dictionary
        print to_list(dictionary.get('filters'))
        filters = [fd(f) for f in to_list(dictionary.get('filters'))]
        order_by = [OrderBy(**o) for o in to_list(dictionary.get('order_by'))]
        fields = to_list(Fields(dictionary.get('fields')))
        return SearchParameters(filters=filters, fields=fields, order_by=order_by)

    def build(self):
        retval = {
            'spec': self._build_spec(),
        }
        if self.sort:
            retval['sort'] = [s.build() for s in self.sort]
        if self.fields:
            retval['fields'] = self.fields.build()
        return retval

    def _build_spec(self):
        s = {}
        for spec in self.spec:
            f = spec.build()
            for k, v in f.iteritems():
                if k in s and isinstance(v, dict):
                    s[k].update(v)
                else:
                    s[k] = v
        return s


class QueryBuilder(object):
    """
    Provides a static function for building PyMongo query arguments based on a
    :class:`SearchParameters` instance.

    Use the static :meth:`create_query` method to create a PyMongo query
    arguments on a given document.
    """
    # TODO: research _create_operation(), _create_filters(), create_query()
    pass
