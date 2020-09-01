# -*- coding: utf-8 -*-
"""
@author: cleartonic
"""
import copy
import csv
import datetime
import json
import logging
import os
import pickle
import random
import shutil
import sys
import time
import traceback
import yaml

from twitchtriviabot.ui import MainWindow

try:
    THIS_FILEPATH = os.path.dirname(__file__)
    THIS_FILENAME = os.path.basename(__file__)
except:
    THIS_FILEPATH = os.path.dirname(sys.executable)
    THIS_FILENAME = os.path.basename(sys.executable)

    
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename=os.path.join(THIS_FILEPATH,'config','output_log.log'),
                filemode='a',
                level=logging.DEBUG)

VERSION_NUM = "2.1.0"

AUTH_CONFIG_PATH=os.path.abspath(os.path.join(THIS_FILEPATH,'config','auth_config.yml'))
TRIVIA_CONFIG_PATH=os.path.abspath(os.path.join(THIS_FILEPATH,'config','trivia_config.yml'))

if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config')))
if not os.path.exists(AUTH_CONFIG_PATH):
    shutil.copyfile(
        os.path.abspath(os.path.join(THIS_FILEPATH,'init_config','auth_config.yml')),
        AUTH_CONFIG_PATH)
if not os.path.exists(TRIVIA_CONFIG_PATH):
    shutil.copyfile(
        os.path.abspath(os.path.join(THIS_FILEPATH,'init_config','trivia_config.yml')),
        TRIVIA_CONFIG_PATH)
if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config','scores'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config','scores')))
if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music')))
    
    with open(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music','track.txt')),'w') as f:
        f.write('Null track')
    with open(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music','artist.txt')),'w') as f:
        f.write('Null artist')


if __name__ == '__main__':
    main_window = MainWindow(VERSION_NUM)
    main_window.window.show()
    main_window.app.exec_()
