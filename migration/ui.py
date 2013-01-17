# -*- coding: utf-8 -*-

import sys
import codecs
import time
from datetime import datetime

stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout)


# Fancy progress ala (pacman) ArchLinux
_colors = {
    'BOLD':   u'\x1b[01;1m',
    'RED':    u'\x1b[01;31m',
    'GREEN':  u'\x1b[01;32m',
    'YELLOW': u'\x1b[01;33m',
    'BLUE':   u'\x1b[01;34m',
    'PINK':   u'\x1b[01;35m',
    'CYAN':   u'\x1b[01;36m',
    'NORMAL': u'\x1b[0m',
    'cursor_on':  u'\x1b[?25h',
    'cursor_off': u'\x1b[?25l',
}

class ProgressBar(object):
    indicator = '\x1b[K%s%s%s\r'
    end_color = _colors['NORMAL']

    def __init__(self, name, total, stream=stdout, suffix=True,
                 color='BOLD', sec_color='BLUE', interval=0.1):
        self.name = name
        self.total = total
        self.start_color = _colors.get(color, _colors['NORMAL'])
        self.sec_start_color = _colors.get(sec_color, _colors['NORMAL'])
        self._interval = interval
        self._last_update = 0
        self._stream = stream
        self._cast = float if suffix and (total > 2040) else type(total)
        self._total_n = self._calc_total_len(total, suffix)
        self._color_n = 2*len(self.start_color) + len(self.sec_start_color) + 3*len(self.end_color)
        if suffix:
            self._format_qty = self._suffix_format_qty
        else:
            self._format_qty = self._simple_format_qty

        self.start_timer()

    def update_state(self, current):
        if time.time() < (self._last_update + self._interval):
            return
        return self.force_update_state(current)

    def finish(self):
        self.force_update_state(self.total, eta=False)
        self._stream.write(u'\n')
        self._stream.flush()

    def force_update_state(self, current, eta=True):
        self._last_update = time.time()
        n = self._total_n
        q = self._format_qty
        sc, ssc, ec = self.start_color, self.sec_start_color, self.end_color
        total = self.total

        pc = (100.*current)/self.total
        eta = self.get_elapsed_time(current=(current if eta else None))
        left = u"%s*%s %s%-22s%s  %s %s  %s [" % (ssc, ec, sc, self.name[:22], ec, q(current), q(total), eta)
        right = u'] %s%3d%%%s' % (sc, pc, ec)

        cols = 22

        ratio = int((cols*current)/total)
        bar = (u'#'*ratio+'-'*cols)[:cols]
        self._stream.write(self.indicator % (left, bar, right))
        self._stream.flush()

    def get_elapsed_time(self, current=None, start=None):
        if start is None: start = self._start
        delta = datetime.now() - start
        if current:
            # estimated time averange
            delta = ((self.total*delta)/current) - delta
        return unicode(delta).split('.')[0]

    def _simple_format_qty(self, qty):
        return (u"%%%dd" % self._total_n) % qty

    def _suffix_format_qty(self, qty):
        sizes = ['K', 'M', 'G', 'T']
        idx = 0
        size = ' '
        while qty > 2048.0:
            qty /= 1024.0
            size = sizes[idx]
            idx += 1

        if self._cast is int: d = '%dd' % self._total_n
        elif self._cast is float: d = '%d.1f' % self._total_n
        else: d = 's'
        return ((u"%%%s%%s" % d) % (self._cast(qty), size)).replace(u".", u",")

    def _calc_total_len(self, total, suffix=False):
        if suffix:
            if self._cast is int:
                return 4
            elif self._cast is float:
                return 6
        return len(str(total))

    def start_timer(self):
        self._start = datetime.now()

NORMAL = _colors['NORMAL']
BOLD = _colors['BOLD']
BLUE = _colors['BLUE']
PINK = _colors['PINK']

INFO = _colors['GREEN']
WARNING = _colors['YELLOW']
ERROR = _colors['RED']

def info(s):
    stdout.write(INFO + u'INFO:' + NORMAL + u" " + s + u"\n")
    stdout.flush()

def warn(s):
    stdout.write(WARNING + u'WARNING:' + NORMAL + u" " + s + u"\n")
    stdout.flush()

def error(s):
    stdout.write(ERROR + u'ERROR:' + NORMAL + u" " + s + u"\n")
    stdout.flush()
    sys.exit(1)

def msg(s):
    stdout.write(BLUE + u'::' + NORMAL + u' ' + BOLD + s + NORMAL + u'\n')
    stdout.flush()

def ptime(s, l=u'tiempo'):
    stdout.write(PINK + u'**' + NORMAL + u' ' + l + u': ' + s + u'\n')

def nl(c=1):
    while c > 0:
        stdout.write(u"\n")
        c -= 1
    stdout.flush()

def report_time(func, *args):
    t0 = datetime.now()
    retval = func(*args)
    t1 = datetime.now()
    t = t1 - t0
    secs = t.days*24*60*60+t.seconds
    mins, sec = divmod(secs, 60)
    hrs, mins = divmod(mins, 60)
    ptime(u"%2dh%2dm%2d.%ss\n" % (hrs, mins, sec, str(t.microseconds)[:3]))
    return retval
