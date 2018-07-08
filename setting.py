# -*-coding=utf-8-*-
# 常用的配置信息

import datetime
import smtplib
from email.mime.text import MIMEText
from sqlalchemy import create_engine
import os
import MySQLdb
import itchat
import json

cfg_file = os.path.join(os.path.dirname(__file__), 'data.cfg')
with open(cfg_file, 'r') as f:
    json_data = json.load(f)

MYSQL_USER = json_data['MYSQL_USER']
MYSQL_USER_Ali = json_data['MYSQL_USER_Ali']
MYSQL_REMOTE_USER = json_data['MYSQL_REMOTE_USER']
MYSQL_PASSWORD = json_data['MYSQL_PASSWORD']
MYSQL_PASSWORD_Ali = json_data['MYSQL_PASSWORD_Ali']
MYSQL_HOST_Ali = json_data['MYSQL_HOST_Ali']
MYSQL_HOST = json_data['MYSQL_HOST']
MYSQL_REMOTE = json_data['MYSQL_REMOTE']
MYSQL_PORT = json_data['MYSQL_PORT']
REDIS_HOST = 'localhost'
EMAIL_USER = json_data['EMAIL_USER']
EMAIL_PASS = json_data['EMAIL_PASSWORD']
SMTP_HOST = json_data['SMTP_HOST']
FROM_MAIL = json_data['FROM_MAIL']
TO_MAIL = json_data['TO_MAIL']
Ali_DB=json_data['Ali_DB']

def get_engine(db):
    # engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, db))
    engine = create_engine(
      'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(MYSQL_REMOTE_USER, MYSQL_PASSWORD, MYSQL_REMOTE,
                                                            MYSQL_PORT, db))
    return engine


def get_mysql_conn(db,local):
    if local:
        conn = MySQLdb.connect(MYSQL_REMOTE, MYSQL_REMOTE_USER, MYSQL_PASSWORD, db, charset='utf8')
    else:
        conn = MySQLdb.connect(MYSQL_HOST_Ali, MYSQL_USER_Ali, MYSQL_PASSWORD_Ali, db, charset='utf8')

    return conn


class MsgSend:
    def __init__(self, name):
        # name为微信要发送的人的微信名称
        self.name = name
        itchat.auto_login(hotReload=True)
        account = itchat.get_friends(self.name)
        self.toName = None
        for i in account:
            if i[u'PYQuanPin'] == self.name:
                self.toName = i['UserName']
        if not self.toName:
            print('print input the right person name')

    def send_price(self, name, real_price, real_percent, types):
        content = name + ' ' + str(real_price) + ' ' + str(real_percent) + ' percent ' + types
        itchat.send(content, toUserName=self.toName)

    def send_ceiling(self, name, vol):
        current = datetime.datetime.now().strftime('%Y %m %d %H:%M %S')
        content = '{} Warning {} : ceiling volume is {}'.format(current, name, vol)
        itchat.send(content, toUserName=self.toName)


def sendmail(content, subject):
    username = EMAIL_USER
    password = EMAIL_PASS
    smtp_host = SMTP_HOST
    smtp = smtplib.SMTP(smtp_host)

    try:
        smtp.login(username, password)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['from'] = FROM_MAIL
        msg['to'] = TO_MAIL
        msg['subject'] = subject
        smtp.sendmail(msg['from'], msg['to'], msg.as_string())
        smtp.quit()
    except Exception, e:
        print(e)


if __name__ == '__main__':
    # msg=MsgSend(u'wei')
    # msg.send_price('hsdq',12,12,'sell')
    # print(FROM_MAIL)
    pass
