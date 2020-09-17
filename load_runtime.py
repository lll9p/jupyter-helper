#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ©Lao https://laolilin.com
# File              : load_runtime.py
# Author            : lll9p <lll9p.china@gmail.com>
# Date              : 29.04.2019
# Last Modified Date: 14.09.2020
# Last Modified By  : lll9p <lll9p.china@gmail.com>

import os
from functools import partial

from runtime_config import (module_dict, plotly_api_key, plotly_username,
                            short_names)


def init(autoreload_num, figure_format, matplotlib, module_groups,
         excludes, random_state, sns_style, data, path, short_names) -> None:
    _globals = globals()
    import argparse
    import importlib
    import sys

    from IPython import get_ipython

    def _import_libs(
        module_groups: list, module_dict: dict, excludes: dict, scope: dict
    ) -> None:
        for module_group in module_groups:
            print(module_group + ": ", end="")
            for (_name, _sub), imp_name in module_dict.get(
                    module_group).items():
                if _name in excludes:
                    continue
                name = _name if _sub is None else "." + _sub
                package = None if _sub is None else _name
                _lib = importlib.import_module(name=name, package=package)
                scope[imp_name] = _lib
                print(
                    f'{_name}{"."+_sub if _sub else ""} as {imp_name}, version:{eval(imp_name+".__version__") if imp_name!="plt" else None}',
                    end=", ",
                )
            print()
        return None

    def run_magics(autoreload_num, figure_format) -> None:
        get_ipython().magic("matplotlib inline")
        get_ipython().magic(
            f"config InlineBackend.figure_format = '{figure_format}'"
        )
        if "autoreload" not in get_ipython().magics_manager.magics["line"]:
            # if autoreload ext was loaded, load it.
            get_ipython().magic("load_ext autoreload")
        get_ipython().magic(f"autoreload {autoreload_num}")
        print(f"Extension autoreload is loaded and set to {autoreload_num} .")
    run_magics(autoreload_num, figure_format)
    _import_libs(
        module_groups=module_groups,
        module_dict=module_dict,
        excludes=excludes,
        scope=_globals,
    )
    styles_dict = {k: v for k, v in (style.split(":")
                                     for style in sns_style.split(','))}
    _globals["random_state"] = random_state
    if short_names["matplotlib"] in _globals:
        # 用来正常显示中文标签
        plt.rcParams['font.sans-serif'] = [
            styles_dict.get("font", "WenQuanYi Micro Hei")]
        plt.rcParams['axes.unicode_minus'] = False
    if short_names["seaborn"] in _globals:
        sns.set(
            context=styles_dict.get("context", "notebook"),
            style=styles_dict.get("style", "ticks"),
            font=styles_dict.get("font", "WenQuanYi Micro Hei"),
            font_scale=float(styles_dict.get("font_scale", 1.2)),
        )
    if short_names["numpy"] in _globals:
        # Set random state, make sure analyse can be reproducing.
        np.random.seed(seed=random_state)
        print(f"The numpy random seed was set to {random_state} .")
    if short_names["sympy"] in _globals:
        sym.init_printing()
        print(f"Sympy pretty printing is enabled.")
    if short_names["plotly"] in _globals:
        plotly.tools.set_credentials_file(
            username=plotly_username, api_key=plotly_api_key
        )
        print(f"Module plotly imported, api username is {plotly_username}")
    # import helpers
    sys.path.append(path)
    _globals["helpers"] = importlib.import_module(name="helpers", package=None)
    print(f"Module helpers has been imported from {current_path}")
    if data is not None:
        helpers.load_from(data, globals())
        print("Data has been loaded.")


def main(_globals: dict, path: str) -> None:
    _globals["init"] = partial(init, path=path, short_names=short_names)


if __name__ == "__main__":
    """
    Useage
    # Init imports and settings.
    %run ../helpers/load_runtime.py \
    --autoreload=1 \
    --figure_format=retina \
    --matplotlib=inline \
    --modules=accelerate,base,plot-plotly \
    --random_state=42 \
    --reset="reset -f in out dhist array" \
    --sns_style="context:notebook,style:ticks,font_scale:1.2,font:WenQuanYi Micro Hei"
    --data="store/data.pbz"
    """
    current_path = os.path.split(os.path.abspath(__file__))[0]
    parent_path = os.path.split(current_path)[0]
    main(_globals=globals(), path=parent_path)