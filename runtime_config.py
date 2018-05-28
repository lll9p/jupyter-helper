#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .plotly_config import plotly_username, plotly_api_key
except ImportError as e:
    plotly_username = ''
    plotly_api_key = ''

short_names = {
    'numexpr': 'ne',
    'numba': 'nb',
    'numpy': 'np',
    'pandas': 'pd',
    'scipy': 'sp',
    'matplotlib': 'mpl',
    'seaborn': 'sns',
    'plotly': 'plotly',
    'sympy': 'sym',
}
# module name, submodule name, import as name
accelerate = {
    ('numexpr', None): 'ne',
    ('numba', None): 'nb',
}
base = {
    ('numpy', None): 'np',
    ('pandas', None): 'pd',
    ('scipy', None): 'sp',
}
ml_sklearn = {
    ('sklearn', 'preprocessing'): 'preprocessing',
    ('sklearn', 'model_selection'): 'model_selection',
}
plot = {
    ('matplotlib', None): 'mpl',
    ('matplotlib', 'pyplot'): 'plt',
    ('seaborn', None): 'sns',
    ('plotly', None): 'plotly',
}
symbol = {
    ('sympy', None): 'sym',
}
module_dict = {
    'accelerate': accelerate,
    'base': base,
    'plot': plot,
    'symbol': symbol,
    'ml_sklearn': ml_sklearn}
