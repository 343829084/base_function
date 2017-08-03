# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
from celery import Celery
ip='10.19.133.255'
broker='redis://%s:6379/5' %ip
backend='redis://%s:6379/6' %ip

app=Celery('tasks',broker=broker,backend=backend)

@app.task
def add(x,y):
    return x+y
