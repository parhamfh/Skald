#!/usr/bin/python
# coding: utf-8

def merge_dicts(a, b):
    '''
        Override any values in dict a that also exist in
        dict b. Applies changes to a in-place.

        Respect dicts in dicts and merges recursively.

        ex:
        Empty sets:

        Single and empty:

        Empty and single:

        Disjoint:
        Nested:
        d1 = {'a':3, 'b':'Adam','C':{'kalas':'tårta','ramsan':'bussar'}}
        d2 = {'b':'Ramses','c':1773,'C': {'kalas':'edge off'}}
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
    print '---'
    print merge_dicts(d1,d2)    

d1 = {'a':3, 'b':'Adam','C':{'kalas':'tårta','ramsan':'bussar'}}
d2 = {'b':'Ramses','c':1773,'C': {'kalas':'edge off'}}
m_n_p(d1,d2)