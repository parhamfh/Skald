# coding: utf8
import os

CURRENT_DIRECTORY = os.path.dirname(__file__)

## SKALD

SKALD_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, '../../'))
SKALD_SRC_DIRECTORY = os.path.join(SKALD_DIRECTORY, 'skald')

SKALD_ASSETS_DIRECTORY = os.path.join(SKALD_DIRECTORY,
    'resources',
    'assets')

skald = {
    'directory': SKALD_DIRECTORY,
    'src': SKALD_SRC_DIRECTORY,
    'assets': SKALD_ASSETS_DIRECTORY,
    'debug': True,
    'logging': 'debug',
    'orpheus_format': 'stdout'
}

## ORPHEUS

ORPHEUS_DIRECTORY = os.path.join(SKALD_DIRECTORY,'contrib','orpheus-skald')
orpheus = {
    'directory': ORPHEUS_DIRECTORY,
    'bin': os.path.join(ORPHEUS_DIRECTORY,'orpheus_v3.4','bin'),
    'output': {
        'folder': os.path.join(ORPHEUS_DIRECTORY,'out'),
        'format': 'stdout',
    }
}
