#!/usr/bin/env python3

import bz2
import pickle


def load_from(file, _globals):
    with bz2.BZ2File(file, 'rb') as f:
        data = pickle.load(f)
        _globals.update(data)
        _globals['data'] = data


def save_to(data, file):
    with bz2.BZ2File(file, "wb") as f:
        pickle.dump(data, f)
