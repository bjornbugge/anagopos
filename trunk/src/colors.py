'''
Color schemes for the OpenGL canvas. Use the "*_color()"-functions to access
the colors in the currently active color scheme.
'''

d = float(255)

color_schemes = {
    'black' : {'arrow'  : (1.0, 0.2, 0.9),
               'line'   : (0.3, 1.0, 0.2),
               'node'   : (0.3, 0.6, 1.0),
               'start'  : (0.5, 0.8, 1.0),
               'nf'     : (1.0, 0.0, 0.0),
               'selfref': (250 / d, 214 / d, 107 / d),
               'newest' : (0.0, 0.0, 1.0),
               'bg'     : (0.0, 0.0, 0.0)},
    'white' : {'arrow'  : (1.0, 36 / d, 0.0),
               'line'   : (0.0, 100 / d, 245 / d),
               'node'   : (0.0, 0.0, 0.0),
               'start'  : (0.0, 100, 127 / d),
               'nf'     : (0xa4 / d, 0.0, 0.0),
               'selfref': (0.4, 0.4, 0.4),
               'newest' : (34 / d, 139 / d,34 / d),
               'bg'     : (1.0, 1.0, 1.0)},
    'grey'  : {'arrow'  : (1.0, 36 / d, 0.0),
               'line'   : (0.0, 100 / d, 245 / d),
               'node'   : (0.0, 0.0, 0.0),
               'start'  : (0.0, 100, 127 / d),
               'nf'     : (0xa4 / d, 0.0, 0.0),
               'selfref': (0.4, 0.4, 0.4),
               'newest' : (34 / d, 139 / d,34 / d),
               'bg'     : (0.5, 0.5, 0.5)}
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
