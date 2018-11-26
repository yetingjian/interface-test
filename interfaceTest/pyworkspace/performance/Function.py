# coding=utf-8

import logging,datetime
import os
import random


def find_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/performance')[0]
    return base + '/performance'

def log(massage):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = find_path() + '/log/'
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=path+'/'+now+'.log')
    logging.info(massage)

def random_mac():
    seed = "1234567890ABCDEF"
    sa = []
    for j in range(12):
        sa.append(random.choice(seed))
    mac = ''.join(sa)
    return mac
