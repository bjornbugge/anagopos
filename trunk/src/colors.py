# -*- coding: utf-8 -*-
'''
Color schemes for the OpenGL canvas. Use the "*_color()"-functions to access
the colors in the currently active color scheme.
'''
# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjoern Bugge Grathwohl and Jens Duelund Pallesen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

d = float(255)

color_schemes = {
    'black' : {'arrow'  : (1.0, 0.2, 0.9),
               'line'   : (0.3, 1.0, 0.2),
               'node'   : (0.3, 0.6, 1.0),
               'start'  : (0.5, 0.8, 1.0),
               'nf'     : (1.0, 0.0, 0.0),
               'selfref': (250 / d, 214 / d, 107 / d),
               'newest' : (0.0, 0.0, 1.0),
               'bg'     : (0.0, 0.0, 0.0),
               'size_op_node'   : [(15, 0.1), (13, 0.2), (11, 0.4), (9, 0.6), (7, 0.8), (5, 1.0)],
               'size_op_start'  : [(15, 0.1), (13, 0.2), (11, 0.4), (9, 0.6), (7, 0.8), (5, 1.0)],
               'size_op_nf'     : [(18, 0.1), (17, 0.2), (15, 0.4), (13, 0.6), (11, 0.8), (9, 1.0)],
               'size_op_newest' : [(15, 0.1), (13, 0.2), (11, 0.4), (9, 0.6), (7, 0.8), (5, 1.0)],
               'size_op_selfref': [(18, 0.22), (17, 0.66), (16, 0.7)],
               'width_op_line'   : [(4.5, 0.2), (2.5, 0.4), (1.5, 0.6), (0.8, 0.3), (0.5, 1.0)]
              },
    'white' : {'arrow'  : (1.0, 36 / d, 0.0),
               'line'   : (0.0, 100 / d, 245 / d),
               'node'   : (0.0, 0.0, 0.0),
               'start'  : (0.0, 100, 127 / d),
               'nf'     : (0xa4 / d, 0.0, 0.0),
               'selfref': (0.4, 0.4, 0.4),
               'newest' : (34 / d, 139 / d,34 / d),
               'bg'     : (1.0, 1.0, 1.0),
               'size_op_node'   : [(7, 1)],
               'size_op_start'  : [(7, 1)],
               'size_op_nf'     : [(12, 1)],
               'size_op_newest' : [(6, 1)],
               'size_op_selfref': [(9, 1)],
               'width_op_line'   : [(1.2, 0.7)]
              },
    'grey'  : {'arrow'  : (1.0, 36 / d, 0.0),
               'line'   : (0.0, 100 / d, 245 / d),
               'node'   : (0.0, 0.0, 0.0),
               'start'  : (0.0, 100, 127 / d),
               'nf'     : (0xa4 / d, 0.0, 0.0),
               'selfref': (0.4, 0.4, 0.4),
               'newest' : (34 / d, 139 / d,34 / d),
               'bg'     : (0.5, 0.5, 0.5),
               'size_op_node'   : [(15, 0.1), (13, 0.2), (11, 0.4), (9, 0.6), (7, 0.8), (5, 1.0)],
               'size_op_start'  : [(15, 0.1), (13, 0.2), (11, 0.4), (9, 0.6), (7, 0.8), (5, 1.0)],
               'size_op_nf'     : [(18, 0.1), (17, 0.2), (15, 0.4), (13, 0.6), (11, 0.8), (9, 1.0)],
               'size_op_newest' : [(15, 0.1), (13, 0.2), (11, 0.4), (9, 0.6), (7, 0.8), (5, 1.0)],
               'size_op_selfref': [(18, 0.22), (17, 0.66), (16, 0.7)],
               'width_op_line'   : [(4.5, 0.2), (2.5, 0.4), (1.5, 0.6), (0.8, 0.3), (0.5, 1.0)]
              }
}

_active_color_scheme = 'black'

def set_color_scheme_black():
    global _active_color_scheme
    _active_color_scheme = 'black'
def set_color_scheme_white():
    global _active_color_scheme
    _active_color_scheme = 'white'
def set_color_scheme_grey():
    global _active_color_scheme
    _active_color_scheme = 'grey'

_fst = lambda l:map(lambda x:x[0], l)
_snd = lambda l:map(lambda x:x[1], l)
def node_sizes():
    return _fst(color_schemes[_active_color_scheme]['size_op_node'])
def node_opacities():
    return _snd(color_schemes[_active_color_scheme]['size_op_node'])
def start_node_sizes():
    return _fst(color_schemes[_active_color_scheme]['size_op_start'])
def start_node_opacities():
    return _snd(color_schemes[_active_color_scheme]['size_op_start'])
def nf_node_sizes():
    return _fst(color_schemes[_active_color_scheme]['size_op_nf'])
def nf_node_opacities():
    return _snd(color_schemes[_active_color_scheme]['size_op_nf'])
def newest_node_sizes():
    return _fst(color_schemes[_active_color_scheme]['size_op_newest'])
def newest_node_opacities():
    return _snd(color_schemes[_active_color_scheme]['size_op_newest'])
def selfref_halo_sizes():
    return _fst(color_schemes[_active_color_scheme]['size_op_selfref'])
def selfref_halo_opacities():
    return _snd(color_schemes[_active_color_scheme]['size_op_selfref'])
def line_widths():
    return _fst(color_schemes[_active_color_scheme]['width_op_line'])
def line_opacities():
    return _snd(color_schemes[_active_color_scheme]['width_op_line'])
def arrow_color():
    return color_schemes[_active_color_scheme]['arrow']
def line_color():
    return color_schemes[_active_color_scheme]['line']
def node_color():
    return color_schemes[_active_color_scheme]['node']
def start_node_color():
    return color_schemes[_active_color_scheme]['start']
def nf_node_color():
    return color_schemes[_active_color_scheme]['nf']
def selfref_halo_color():
    return color_schemes[_active_color_scheme]['selfref']
def newest_node_color():
    return color_schemes[_active_color_scheme]['newest']
def background_color():
    return color_schemes[_active_color_scheme]['bg']
