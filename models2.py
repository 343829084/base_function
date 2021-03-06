# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, Text,ForeignKey
from sqlalchemy import event
from sqlalchemy import DDL
engine = create_engine('mysql+pymysql://root:@localhost:3306/db_parker?charset=utf8')
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class House(Base):
    __tablename__ = 'tb_houses'

    id = Column(Integer, primary_key=True)
    house_name = Column(String(80),index=True)
    city_name = Column(String(80),index=True)
    url = Column(String(300),index=True)
    price = relationship('Price',backref='houseinfo')
    rent_info = relationship('Rent',backref='houseinfo')
    latitude = Column(String(50))
    longitude = Column(String(50))
    address = Column(String(300))
    building_date = Column(String(60))
    building_type = Column(String(60))
    property_corp = Column(Text)
    developers = Column(Text)
    district = Column(String(60))

event.listen(
        House.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1000000;")
    )

class Price(Base):
    __tablename__ = 'tb_prices'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    origin = Column(String(80),index=True)
    months = Column(String(80))
    crawl_time = Column(DateTime)
    uid= Column(Integer,ForeignKey('tb_houses.id'))

class Rent(Base):
    __tablename__ = 'tb_rents'
    id = Column(Integer, primary_key=True)
    rent_price = Column(Integer,index=True)
    rent_origin = Column(String(80),index=True)
    publish_date = Column(DateTime,index=True)
    rent_crawl_time = Column(DateTime)
    rent_type=Column(String(80))
    house_type=Column(String(80))
    rent_floor = Column(String(80))
    rent_url=Column(String(600))
    rent_title= Column(Text)
    rent_area=Column(String(80))
    uid= Column(Integer,ForeignKey('tb_houses.id'))

Base.metadata.create_all(engine)



session=DBSession()
#d=session.query(House).filter(House.house_name ==u'丽都花园').filter(House.city_name ==u'东莞').first()
urls_info = session.query(House.id, House.url).join(Price).filter(Price.origin == 'FTX').filter(
    House.url.like('%m.fang.com%')).filter(
    House.city_name == '保定').all()

for i in urls_info:
    #print(i[1])
    try:
        hostid = re.findall('/(\d+)\.htm', i[1])[0]
        print(hostid)
    except:
        pass
#print(d.building_date)
#if d.building_date==u'暂无数据':
    #d.building_date=u'2017年'
'''
for i in d:
    print(i.price)
    #session.delete(i)
'''
session.commit()
session.close()
