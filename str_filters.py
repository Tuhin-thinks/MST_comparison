import re
from ast import literal_eval

from config import ConfigSingleton

config = ConfigSingleton()


def num_filtering(string: str):
    """Filter value."""
    _value = string
    if type(string) == str:
        _value = string.strip("\n").strip("\r\t ")

    try:
        _value = round(float(_value), config.N_DECIMALS)
    except ValueError:
        return False, _value

    return True, _value


def check_iterable(string: str):
    # match with list or tuple
    iterable_pattern = r"([\[|\(])(-?\d(\.?\d+)?).*([\)|\]])"
    if re.match(iterable_pattern, string):
        try:
            temp_iterable = literal_eval(string.replace(" ", ",") if "," not in string else string)
            new_iterable = []
            for item in temp_iterable:
                _, item = num_filtering(item)
                new_iterable.append(item)
            return new_iterable
        except SyntaxError:
            pass

    # match with dict
    ratio_pattern = r"(-?\d(\.?\d+)?)\:(-?\d(\.?\d+)?)"
    if re.match(ratio_pattern, string):
        try:
            parts = string.split(":")
            if len(parts) == 2:
                return {num_filtering(parts[0])[1], num_filtering(parts[1])[1]}
            return string
        except SyntaxError:
            pass


def filter_value(string: str):
    """Filter any given mst value."""
    string = string.strip("\n").strip("\r\t ")
    is_num, value = num_filtering(string)
    if is_num:
        return value
    else:
        return check_iterable(string)
