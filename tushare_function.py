#-*-coding=utf-8-*-
__author__ = 'rocchen'
import tushare as ts

#df=ts.get_hist_data('300141',start='2011-01-01',end='2016-7-13')
#�������ֻ�ܻ�ȡ��3�������
#print df

stock_info=ts.get_stock_basics()

data=stock_info.ix['300141']['timeToMarket']
print data
print type(data)
data=str(data)
print type(data)
print data[1:4]
print data[4:6]
print data
date_format=data[0:4]+'-'+data[4:6]+'-'+data[6:8]
print date_format
#���ڵĸ�ʽ����ת��

'''
data="20101112"
index=0
for i in data:
    print index
    print i
    index=index+1
print data[1:3]
'''
df = ts.get_h_data('300141',start=date_format,end="2016-07-12")
#����������Ի�ȡ���е���ʷ����
print df
print df.dtypes
