#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ©Lao https://laolilin.com
# File              : runtime_config.py
# Author            : lll9p <lll9p.china@gmail.com>
# Date              : 29.04.2019
# Last Modified Date: 29.04.2019
# Last Modified By  : lll9p <lll9p.china@gmail.com>

try:
    from .plotly_config import plotly_username, plotly_api_key
except ImportError:
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
