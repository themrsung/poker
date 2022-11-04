# UTILITIES

def get_index_of_dict_value(dict, val):
    vals = list(dict.values())
    keys = list(dict.keys())
    return keys[vals.index(val)]