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

def m_n_p(d1,d2):
    print 'd1 pre-merge: ',d1
    print 'd2 pre-merge: ',d2
    print 'Merged: ',merge_dicts(d1,d2)
    print '---'

# Empty sets:
print 'Empty sets:'
m_n_p({}, {})

# Single and empty:
print 'Single and empty:'
m_n_p({'adam':'333'}, {})

# Empty and single:
print 'Empty and single:'
m_n_p({},{"kalasbjörnar":77})

# Meeting sets
print 'Meeting sets:'
m_n_p({'':22,77:'movies','anchor':'hawk','batman':'bruce','robin':'helper'},{'':'satan','movies':77,'anchor':'bear'})
# Disjoint:
print 'Disjoint:'
m_n_p({'a':1,1:'a'},{'b':2,2:'b'})

# Nested:
print 'Nested:'
d1 = {'a':3, 'b':'Adam','C':{'kalas':'tårta','ramsan':'bussar'}}
d2 = {'b':'Ramses','c':1773,'C': {'kalas':'edge off'}}
m_n_p(d1,d2)

