'''
Created on Feb 8, 2013

@author: parhamfh
'''

class Mockable(object):
    
    def __new__(cls, *args, **kwargs):
        
        if kwargs.pop('mock', None):
            mock_cls = eval('{0}{1}'.format('Mock',cls.__name__))
            print mock_cls
            return super(mock_cls, mock_cls).__new__(mock_cls)
        
        return super(cls, cls).__new__(cls,*args, **kwargs)


class MockableMetaclass(type):
    
    def __call__(self, *args, **kwargs):
        print 'making the call'
        obj = self.__new__(self, *args, **kwargs)
        print 'not maked call'
        if "mock" in kwargs:
            del kwargs["mock"]
        
        obj.__init__(*args, **kwargs)
        
        return obj