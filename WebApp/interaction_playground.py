# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 22:38:18 2018

@author: ASUS
"""
from random import random

from bokeh.layouts import row
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure, output_file, show

x = [random() for x in range(10)]
y = [random() for y in range(10)]

source = ColumnDataSource(data = dict(x=x, y=y))

p = figure(plot_width=400, plot_height=400)
p.circle('x','y', source = source, size = 10)

show(p)