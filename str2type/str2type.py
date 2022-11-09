from functools import singledispatch
from typing import Any
import importlib

@singledispatch
def get_type(name):
    raise TypeError(f"Cannot convert {name} to a type!")

@get_type.register
def _(name: str):
    if len( (s := name.split("."))) > 1:
        return _get_external_type(s)

    try:
        type_ = eval(name)
        if type(type_) != type:
            raise NameError
    except NameError:
        raise TypeError(f"Passed value {name} does not match any built-in python types!")
    return type_

@get_type.register
def _(name: type):
    return name

@get_type.register
def _(name: list):
    return [get_type(n) for n in name]

def _get_external_type(t):
    clname = t[-1]
    modname = ".".join(t[:-1])
    mod = importlib.import_module(modname)
    t_ = getattr(mod, clname)
    if type(t_) != type:
        raise TypeError(f"Passed value {t[-1]} does not match any types in module {modname}!")

    return t_
    

def _check(t: type, value: Any):
    try:
        t(value)
    except (ValueError, TypeError):
        raise TypeError(f"Type {type(value).__name__} cannot be cast as type {t.__name__}")
    return True


@singledispatch
def check_type(t: str, value: Any):
    t_ = get_type(t)
    return _check(t_, value)

@check_type.register
def _(t: type, value: any):
    return _check(t, value)

@check_type.register
def _(t: list, value: Any):
    types = get_type(t)
    for t_ in types:
        try:
            matches = check_type(t_, value)
            return True
        except TypeError:
            continue
    raise TypeError(f"Value {value} cannot be cast as any of the types in {types}")

def parse_types(data: dict):
    new_data = {}
    for key, value in data.items():
        if type(value) == dict:
            new_data.update({key: parse_types(value)})
        else:
            try:
                new_data.update({key: get_type(value)})
            except TypeError:
                new_data.update({key: value})
    return new_data
