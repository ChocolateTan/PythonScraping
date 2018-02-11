# -*- coding: UTF-8 -*-
import os

PATH_APP_ROOT = ''
PATH_CACHE_ROOT = ''
PATH_CACHE_DOWNLOAD = ''
PATH_CACHE_DATA = ''

SAVE_FILE_NAME = ''


class Init:
    def __init__(self):
        global PATH_APP_ROOT
        global PATH_CACHE_ROOT
        global PATH_CACHE_DOWNLOAD
        global PATH_CACHE_DATA
        global SAVE_FILE_NAME

        PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        PATH_CACHE_ROOT = '{0}/cache'.format(PATH_APP_ROOT)
        PATH_CACHE_DOWNLOAD = '{0}/downloads'.format(PATH_CACHE_ROOT)
        PATH_CACHE_DATA = '{0}/data'.format(PATH_CACHE_ROOT)
        SAVE_FILE_NAME = 'BookInfo'

        print '\n--------- Global Values'
        print '\n---------'
        print 'init GlobalList.PATH_APP_ROOT', PATH_APP_ROOT
        print 'init GlobalList.PATH_CACHE_ROOT', PATH_CACHE_ROOT
        print 'init GlobalList.PATH_CACHE_DOWNLOAD', PATH_CACHE_DOWNLOAD
        print 'init GlobalList.PATH_CACHE_DATA', PATH_CACHE_DATA
        print '---------\n'
