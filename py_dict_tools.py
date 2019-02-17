__author__ = 'bdhimes

def nested_dict_builder(*args, bottom_level={}):
    """
    creates a nested dictionary as many levels deep as lists you
    supply, recursively adding each dictionary
    """ 
    d = {x: bottom_level for x in args[0]}
    for each in args[1:]:
        new_d = {title: d for title in each}
        d = new_d.copy()
    return d


def lookup_and_delete(dictionary, inner_key, item_to_find):
    """
    deletes the first instance of an item found in your dictionary, 
    within the specified key that can exist at any nested layer
    """
    for x in dictionary.values():
        if inner_key in x.keys():
            for y in x.values():
                if item_to_find in y:
                    x[inner_key].remove(item_to_find)
                    return True
        else:
            lookup_and_delete(x, inner_key, item_to_find)
    return False
