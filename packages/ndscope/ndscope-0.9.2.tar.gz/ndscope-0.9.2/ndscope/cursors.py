# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np

import pyqtgraph as pg
try:
    from qtpy.QtCore import Qt
except ImportError:
    from PyQt5.QtCore import Qt

from . import util


LABEL_FILL = (0, 0, 0, 200)


class Crosshair:
    __slots__ = [
        '__weakref__',
        'hline', 'vline', 'label',
        'active_plot',
    ]

    pen = pg.mkPen(style=Qt.DotLine)

    def __init__(self):
        """crosshair needs scope to get t0 value"""
        self.hline = pg.InfiniteLine(
            angle=0,
            pen=self.pen,
            movable=False,
        )
        self.vline = pg.InfiniteLine(
            angle=90,
            pen=self.pen,
            movable=False,
        )
        self.label = pg.TextItem(
            anchor=(1, 1),
            fill=LABEL_FILL,
        )
        self.active_plot = None

    def set_active_plot(self, plot):
        if plot == self.active_plot:
            return
        if self.active_plot:
            self.active_plot.removeItem(self.hline)
            self.active_plot.removeItem(self.vline)
            self.active_plot.removeItem(self.label)
            self.active_plot = None
        if plot:
            plot.addItem(self.hline)
            plot.addItem(self.vline)
            plot.addItem(self.label)
            self.active_plot = plot

    def update(self, pos, plot, t0):
        self.set_active_plot(plot)
        ppos = plot.vb.mapSceneToView(pos)
        x = ppos.x()
        y = ppos.y()
        (xmin, xmax), (ymin, ymax) = plot.viewRange()
        if x > (xmin+xmax)/2:
            ax = 1
        else:
            ax = 0
        if y < (ymin+ymax)/2:
            ay = 1
        else:
            ay = 0
        t = t0 + x
        self.hline.setPos(y)
        self.vline.setPos(x)
        self.label.setPos(x, y)
        self.label.setAnchor((ax, ay))
        greg = util.gpstime_str_greg(util.gpstime_parse(t), '%Y/%m/%d %H:%M:%S %Z')
        label = '''<table>
<tr><td rowspan="2" valign="middle">T=</td><td>{:0.3f}</td></tr>
<tr><td>{}</td></tr>
<tr><td>Y=</td><td>{:g}</td></tr>
</table></nobr>'''.format(t, greg, y)
        self.label.setHtml(label)


class TCursors:
    __slots__ = [
        '__weakref__',
        'plots',
    ]

    def __init__(self):
        self.plots = []

    def add_plot(self, plot):
        lines = []
        for index, label in enumerate(['T1', 'T2']):
            cur = pg.InfiniteLine(
                angle=90,
                pen=pg.mkPen(style=Qt.DashLine),
                movable=True,
                label=label,
                labelOpts={
                    'position': 0,
                    'anchors': [(0, 1), (1, 1)],
                    'fill': LABEL_FILL,
                },
            )
            cur._cursor_index = index
            cur.sigPositionChanged.connect(self.update_line)
            lines.append(cur)
        diff = pg.InfiniteLine(
            angle=90,
            pen=(0, 0, 0, 0),
            label='diff',
            labelOpts={
                'position': 1,
                'anchors': [(0.5, 0), (0.5, 0)],
                'fill': LABEL_FILL,
            },
        )
        self.plots.append((plot, lines, diff))

    def enable(self):
        for plot, lines, diff in self.plots:
            for line in lines:
                plot.addItem(line)
            plot.addItem(diff)
        self.reset()

    def disable(self):
        for plot, lines, diff in self.plots:
            for line in lines:
                plot.removeItem(line)
            plot.removeItem(diff)

    def set_value(self, index, value):
        label = None
        for plot, lines, diff in self.plots:
            lines[index].setValue(value)
            lines[index].label.setText('{:g}'.format(value))
            if not label:
                l0 = lines[0].value()
                l1 = lines[1].value()
                diff_pos = (l0 + l1)/2
                diff_val = np.abs(l1 - l0)
                label = u'<table><tr><td rowspan="2" valign="middle">ΔT=</td><td>{:g} s</td></tr><tr><td>{:g} Hz</td></tr></table></nobr>'.format(
                    diff_val, 1/diff_val)
            diff.setValue(diff_pos)
            diff.label.setHtml(label)

    def update_line(self, line):
        value = line.value()
        index = line._cursor_index
        self.set_value(index, value)

    def reset(self):
        try:
            plot = self.plots[0][0]
        except IndexError:
            return
        x, y = plot.viewRange()
        self.set_value(0, (2*x[0] + x[1])/3)
        self.set_value(1, (x[0] + 2*x[1])/3)


class YCursors:
    __slots__ = [
        '__weakref__',
        'Y1', 'Y2', 'diff', 'plot',
    ]

    def __init__(self):
        pen = pg.mkPen(style=Qt.DashLine)
        label_opts = {
            'position': 0,
            'anchors': [(0, 0), (0, 1)],
            'fill': LABEL_FILL,
        }
        self.Y1 = pg.InfiniteLine(
            angle=0,
            pen=pen,
            movable=True,
            label='Y1',
            labelOpts=label_opts,
        )
        self.Y2 = pg.InfiniteLine(
            angle=0,
            pen=pen,
            movable=True,
            label='Y2',
            labelOpts=label_opts,
        )
        self.Y1.sigPositionChanged.connect(self.update_line)
        self.Y2.sigPositionChanged.connect(self.update_line)
        self.diff = pg.InfiniteLine(
            angle=0,
            pen=(0, 0, 0, 0),
            label='diff',
            labelOpts={
                'position': 1,
                'anchors': [(1, 0.5), (1, 0.5)],
                'fill': LABEL_FILL,
            },
        )
        self.plot = None

    def set_plot(self, plot):
        if plot == self.plot:
            return
        if self.plot:
            self.plot.removeItem(self.Y1)
            self.plot.removeItem(self.Y2)
            self.plot.removeItem(self.diff)
        if plot:
            plot.addItem(self.Y1)
            plot.addItem(self.Y2)
            plot.addItem(self.diff)
        self.plot = plot
        self.reset()

    def update_line(self, line):
        value = line.value()
        line.label.setText('{:g}'.format(value))
        l0 = self.Y1.value()
        l1 = self.Y2.value()
        self.diff.setValue((l0 + l1)/2)
        vdiff = np.abs(l1 - l0)
        label = u'ΔY={:g}'.format(vdiff)
        self.diff.label.setText(label)

    def reset(self):
        if not self.plot:
            return
        x, y = self.plot.viewRange()
        y1 = (2*y[0] + y[1])/3
        y2 = (y[0] + 2*y[1])/3
        self.Y1.setValue(y1)
        self.Y2.setValue(y2)
