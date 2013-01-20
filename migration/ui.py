#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
from datetime import datetime

_colors = {
    'BOLD':   '\x1b[01;1m',
    'RED':    '\x1b[01;31m',
    'GREEN':  '\x1b[32m',
    'YELLOW': '\x1b[33m',
    'PINK':   '\x1b[35m',
    'BLUE':   '\x1b[01;34m',
    'CYAN':   '\x1b[36m',
    'NORMAL': '\x1b[0m',
    'cursor_on': '\x1b[?25h',
    'cursor_off': '\x1b[?25l',
}

class ProgressBar(object):
    rot_idx = 0
    rot_chr = ['\\', '|', '/', '-']
    indicator = '\x1b[K%s%s%s\r'
    end_color = _colors['NORMAL']

    def __init__(self, name, total, stream=sys.stdout, suffix=False, color=None, sec_color=None):
        self.name = name
        self.total = total
        self.start_color = _colors.get(color, _colors['NORMAL'])
        self.sec_start_color = _colors.get(sec_color, _colors['NORMAL'])
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
        n = self._total_n
        q = self._format_qty
        sc, ssc, ec = self.start_color, self.sec_start_color, self.end_color
        total = self.total
        self.rot_idx += 1
        ind = self.rot_chr[self.rot_idx % 4]

        pc = (100.*current)/self.total
        eta = self.get_elapsed_time()
        left = "[%s/%s][%s%2d%%%s][%s%s%s][" % (q(current), q(total), sc, pc, ec, ssc, ind, ec)
        right = '][%s%s%s]' % (sc, eta, ec)

        cols = 80 - len(left)  - len(right) + self._color_n
        if cols < 7: cols = 7

        ratio = int((cols*current)/total) - 1
        bar = ('='*ratio+'>').ljust(cols)
        self._stream.write(self.indicator % (left, bar, right))
        self._stream.flush()

    def get_elapsed_time(self, start=None):
        """
        Format a time delta (datetime.timedelta) using the format DdHhMmS.MSs
        """
        if start is None: start = self._start
        delta = datetime.now() - start
        days = int(delta.days)
        hours = int(delta.seconds / 3600)
        minutes = int((delta.seconds - hours * 3600) / 60)
        seconds = delta.seconds - hours * 3600 - minutes * 60 \
                + float(delta.microseconds) / 1000 / 1000
        result = ''
        if days: result += '%dd' % days
        if days or hours: result += '%dh' % hours
        if days or hours or minutes: result += '%dm' % minutes
        return '%s%.3fs' % (result, seconds)

    def _simple_format_qty(self, qty):
        return ("%%%dd" % self._total_n) % qty

    def _suffix_format_qty(self, qty):
        sizes = ['K', 'M', 'G', 'T']
        idx = 0
        size = ''
        while qty > 2048.0:
            qty /= 1024.0
            size = sizes[idx]
            idx += 1

        if self._cast is int: d = '%dd' % self._total_n
        elif self._cast is float: d = '%d.1f' % self._total_n
        else: d = 's'
        return ("%%%s%%s" % d) % (self._cast(qty), size)

    def _calc_total_len(self, total, suffix=False):
        if suffix:
            if self._cast is int:
                return 4
            elif self._cast is float:
                return 6
        return len(str(total))

    def start_timer(self):
        self._start = datetime.now()

    def finish(self):
        self._stream.write(u'\n')
        self._stream.flush()


class PacmanProgress(ProgressBar):

    def get_elapsed_time(self, start=None):
        if start is None: start = self._start
        return str(datetime.now() - start).split('.')[0]

    def update_state(self, current):
        n = self._total_n
        q = self._format_qty
        sc, ssc, ec = self.start_color, self.sec_start_color, self.end_color
        total = self.total
        self.rot_idx += 1
        ind = self.rot_chr[self.rot_idx % 4]

        pc = (100.*current)/self.total
        eta = self.get_elapsed_time()
        left = "%s*%s %s%-26s%s  %s %s  %s [" % (ssc, ec, sc, self.name[:22], ec, q(current), q(total), eta)
        right = '] %s%3d%%%s' % (sc, pc, ec)

        cols = 26

        ratio = int((cols*current)/total)
        bar = ('#'*ratio+'-'*cols)[:cols]
        self._stream.write(self.indicator % (left, bar, right))
        self._stream.flush()

if __name__ == '__main__':
    bar = ProgressBar('testing bar', 512)
    for i in xrange(512+1):
        bar.update_state(i)
        time.sleep(0.01)
    bar.finish()

    bar = ProgressBar('big test', 1024*1024*8)
    for i in xrange(0, 1024*1024*8+1, 1024*1024/64):
        bar.update_state(i)
        time.sleep(0.01)
    bar.finish()

    bar = PacmanProgress('esto es algo que tiene que ser bastante largo', 1024*1024*1024*8, suffix=True, color='BOLD', sec_color='BLUE')
    for i in xrange(0, 1024*1024*8+1, 1024*1024/64):
        bar.update_state(i*1024)
        time.sleep(0.01)
    bar.finish()
