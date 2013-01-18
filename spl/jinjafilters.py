# -*- coding: utf-8 -*-

from decimal import Decimal
from spl.utils import json, ModelJSONEncoder

def dateformat_filter(date, format="%d %b, %Y"):
    if date:
        return date.strftime(format)
    return ''

def moneyftm_filter(value, places=2, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg=''):
    q = Decimal(10) ** -places
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))

def tojson_filter(obj):
    return json.dumps(obj, cls=ModelJSONEncoder)

def configure_jinjafilters(app):
    app.jinja_env.filters['dateformat'] = dateformat_filter
    app.jinja_env.filters['moneyfmt'] = moneyftm_filter
    app.jinja_env.filters['tojson'] = tojson_filter
