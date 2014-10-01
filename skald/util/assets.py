# coding: utf8
import os
import os.path
import inspect

import skald.config as config

ASSETS_FOLDER = config.environment['assets'] 

def get_class_asset_folder(caller_cls):
    # do some magic
    module  = inspect.getmodule(caller_cls[1][0])
    
    # get only the actual module name, not full path
    short_module_name = module.__name__.split('.')[-1]
    return short_module_name


def get_my_file(filename, mode=None):

    # get caller class/module name and translate 

    module_name = get_class_asset_folder(inspect.stack())
    # join paths
    # Set env for assets folder and use that
    
    print 'module name is : ', module_name
    p = os.path.join(ASSETS_FOLDER, module_name, filename)

    # Mode
    if not mode:
        file_mode = 'r'
    else:
        file_mode = mode
    
    f = open(p,file_mode)
    
    return f


