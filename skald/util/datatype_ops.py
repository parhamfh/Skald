#!/usr/bin/python
# coding: utf-8

def merge_dicts(a, b):
    '''
        Override any values in dict a that also exist in
        dict b. Applies changes to a in-place.

        Respect dicts in dicts and merges recursively.

        Ex:
            Empty sets:
            d1 pre-merge:  {}
            d2 pre-merge:  {}
            Merged:  {}
            
            Single and empty:
            d1 pre-merge:  {'adam': '333'}
            d2 pre-merge:  {}
            Merged:  {'adam': '333'}
            
            Empty and single:
            d1 pre-merge:  {}
            d2 pre-merge:  {'kalasbj\xc3\xb6rnar': 77}
            Merged:  {'kalasbj\xc3\xb6rnar': 77}
            
            Meeting sets:
            d1 pre-merge:  {'': 22, 'batman': 'bruce', 'robin': 'helper', 77: 'movies', 'anchor': 'hawk'}
            d2 pre-merge:  {'': 'satan', 'movies': 77, 'anchor': 'bear'}
            Merged:  {'': 'satan', 'batman': 'bruce', 77: 'movies', 'anchor': 'bear', 'movies': 77, 'robin': 'helper'}
            
            Disjoint:
            d1 pre-merge:  {'a': 1, 1: 'a'}
            d2 pre-merge:  {2: 'b', 'b': 2}
            Merged:  {'a': 1, 1: 'a', 2: 'b', 'b': 2}
            
            Nested:
            d1 pre-merge:  {'a': 3, 'C': {'ramsan': 'bussar', 'kalas': 't\xc3\xa5rta'}, 'b': 'Adam'}
            d2 pre-merge:  {'c': 1773, 'b': 'Ramses', 'C': {'kalas': 'edge off'}}
            Merged:  {'a': 3, 'C': {'ramsan': 'bussar', 'kalas': 'edge off'}, 'b': 'Ramses', 'c': 1773}
    '''
    for key in b:
        
        if key not in a:
            a[key] = b[key]

        else:
            if isinstance(a[key],dict):
                a[key] = merge_dicts(a[key],b[key])

            else:
                a[key] = b[key]
    return a

def is_int(int_candidate):
    try:
        int(int_candidate)
        return True
    except ValueError:
        return False