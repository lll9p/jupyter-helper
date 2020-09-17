#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ©Lao https://laolilin.com
# File              : load_runtime.py
# Author            : lll9p <lll9p.china@gmail.com>
# Date              : 29.04.2019
# Last Modified Date: 29.04.2019
# Last Modified By  : lll9p <lll9p.china@gmail.com>

import argparse
import importlib
import importlib.util
import os
import sys

from IPython import get_ipython

from runtime_config import (module_dict, plotly_api_key, plotly_username,
                            short_names)


def _import_libs(
    module_groups: list, module_dict: dict, excludes: dict, scope: dict
) -> None:
    for module_group in module_groups:
        print(module_group + ": ", end="")
        for (_name, _sub), imp_name in module_dict.get(module_group).items():
            if (_name, _sub) in excludes:
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


def get_module(module_arg: str) -> (list, list):
    module_groups, excludes = [], []
    for module_opt in module_arg.split(sep=","):
        _ = module_opt.split("-")
        module_groups.append(_.pop(0))
        for exclude in _:
            __ = exclude.split(sep=".", maxsplit=1)
            if len(__) != 2:
                __.append(None)
            excludes.append(tuple(__))
    return module_groups, excludes


def get_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--autoreload", type=int, default="2")
    parser.add_argument("--figure_format", type=str, default="retina")
    parser.add_argument("--matplotlib", type=str, default="inline")
    parser.add_argument("--modules", type=str, default="base")
    parser.add_argument("--random_state", type=int, default="42")
    parser.add_argument("--sns_style", type=str, default="context:notebook")
    parser.add_argument(
        "--reset", type=str, default="reset -f in out dhist array"
    )
    parser.add_argument("--data", type=str)

    args = parser.parse_args()

    autoreload_num = args.autoreload
    figure_format = args.figure_format
    module_arg = args.modules
    random_state = args.random_state
    sns_style = args.sns_style.split(",")
    data = args.data
    styles_dict = {k: v for k, v in (style.split(":") for style in sns_style)}
    return (
        autoreload_num,
        figure_format,
        module_arg,
        random_state,
        sns_style,
        styles_dict,
        data,
    )


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


def main(_globals: dict) -> None:
    current_path = os.path.split(__file__)[0]
    parent_path = os.path.split(current_path)[0]
    autoreload_num, figure_format, module_arg, random_state, sns_style, styles_dict, data = (
        get_args()
    )
    run_magics(autoreload_num, figure_format)
    module_groups, excludes = get_module(module_arg)
    _import_libs(
        module_groups=module_groups,
        module_dict=module_dict,
        excludes=excludes,
        scope=_globals,
    )
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
    sys.path.append(parent_path)
    _globals["helpers"] = importlib.import_module(name="helpers", package=None)
    print(f"Module helpers has been imported from {current_path}")
    if data != "None":
        helpers.load_from(data, globals())
        print("Data has been loaded.")


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
    main(_globals=globals())