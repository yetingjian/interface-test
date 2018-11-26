# coding=utf-8
from selenium import webdriver
import logging,datetime
import os
import random,string



def find_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/x_Agent_API')[0]
    return base + '/x_Agent_API'


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


def get_now_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    return str(year) + str(month) + str(day)


def random_num():
    return random.randint(10000000, 99999999)


def random_string():
    return string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i',
                                      'h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9'], 10)).replace(" ","")


