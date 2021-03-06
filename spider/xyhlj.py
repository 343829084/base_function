# -*-coding=utf-8-*-
import random
import re
import time
import requests
import json
from lxml import etree
import pymongo

db = pymongo.MongoClient('localhost')
doc = db['NEXGO']['HLJSXR']


def get_proxy(retry=5):
    proxyurl = 'http://:8081/dynamicIp/common/getDynamicIp.do'
    count = 0
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=5)
        except Exception as e:
            print(e)
            count += 1
            print('代理获取失败,重试' + str(count))
            time.sleep(1)
        else:
            js = r.json()
            proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
            proxies_random = {
                'http': proxyServer
            }
            print(proxies_random)
            return proxies_random



session = requests.Session()


class Spider(object):

    def __init__(self):
        self.post_url = 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc='

        self.ua = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:39.0) Gecko/20100101 Firefox/39.0"
        self.cookie = "JSESSIONID=D1ti3Ic-k5y4WH-AfiT4YXS4SXvibGwQcUZABzgo0mu68Wpk5nlg!651693374"
        self.origin_url = 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=&proselect=&cityselect=&disselect='
        self.refer = "http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc="

    def loop(self):
        for i in range(1, 100):
            self.get_list(i)

    def get_list(self, page):
        post_data = {'proselect': "", 'cityselect': "", 'disselect': "", 'curPageNO': str(page)}
        req_header = {
            'Host': 'www.hljcredit.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=',
            # 'Cookie': 'JSESSIONID=IdJ909qBdOc3wMUGEhiuR78EjKAYWnYwR8qx3YDOgC1VU1cSJ_wg!-2075877866',
            'Connection': 'keep-alive',
            # 'Pragma': 'no-cache'
        }
        first_proxy={}
        first_proxy=get_proxy()
        try:
            s = session.post(self.post_url, headers=req_header, data=post_data,proxies=first_proxy)
        except Exception as e:
            print(e)
        response = etree.HTML(s.text)
        nodes = response.xpath('//table[@class="list_2_tab"]/tr')
        # print('find the list')
        print('lens of nodes ',len(nodes))
        for node in nodes[1:]:
            print('find the list')
            url_pattern = node.xpath('.//td[2]/a/@href')[0]
            if url_pattern is None:
                url = None
            else:
                url = 'http://www.hljcredit.gov.cn/' + url_pattern
            try:
                p_headers = {
                    'Host': 'www.hljcredit.gov.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    # 'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=',
                    # 'Cookie': 'JSESSIONID=IdJ909qBdOc3wMUGEhiuR78EjKAYWnYwR8qx3YDOgC1VU1cSJ_wg!-2075877866',
                    'Connection': 'keep-alive',
                    # 'Pragma': 'no-cache'
                }
                column_name = ['case_number', 'person_name', 'sex', 'age', 'identify_number', 'enterprise_name', 'area',
                               'executed_court', 'executed_number', 'executed_unit',
                               'execution', 'execution_detail', 'executed_item', 'not_execute', 'case_date',
                               'release_date']
                time.sleep(random.random() * 10)
                ss = session.get(url, headers=p_headers,proxies=first_proxy,cookies=self.cookie)
                # print(ss.text)
                resp = etree.HTML(ss.text)
                item_list = resp.xpath('//table[@class="for_letter"]/tr')
                # for each_item in item_list:
                item = {}
                for index, value in enumerate(column_name):
                    item[value] = item_list[index].xpath('.//td[2]/text()')[0].strip()
                doc.insert(item)

            except Exception as e:
                print(e)

        print('done')

    def gets(self):

        r = session.get(self.url, headers=self.headers)
        print('Cookie::{}'.format(r.cookies))
        tree = etree.HTML(r.text)
        return r.text, tree

    def _gets(self, url):
        get_header = {
            'Host': 'www.hljcredit.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Cookie': self.cookie
        }
        r = requests.get(url, headers=get_header, cookies={'Cookie': self.cookie})
        return r.text

    def posts(self, page):
        post_header = {
            'Host': 'www.hljcredit.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            # 'Cookie':self.cookie
        }
        post_data = {'proselect': "", 'cityselect': "", 'disselect': "", 'curPageNO': str(page)}
        r = requests.post(self.post_url, headers=post_header, data=post_data

                          )
        text = r.text
        tree = etree.HTML(r.text)
        return text, tree

    def download(self):
        r = requests.get(self.url)
        filename = 'code.png'
        with open(filename, 'wb') as f:
            f.write(r.content)

    '''
    def person_post_action(self):
        login_header = {
            'Host': 'www.hljcredit.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Connection': 'keep-alive',
        }

        url1 = 'http://www.hljcredit.gov.cn/regController.do?checkislogin'
        data1 = {'checklogin': ''}
        self.session.post(url=url1, headers=login_header, data=data1, proxies=get_proxy())
        url2 = 'http://www.hljcredit.gov.cn/flowCalculateController.do?index'
        data2 = {'cmain': 'xycx', 'flowname': 'xyhlj'}
        flow_header = {
            'Host': 'www.hljcredit.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Connection': 'keep-alive',
        }
        self.session.post(url=url2, headers=flow_header, data=data2, proxies=get_proxy())
    '''

    def parse(self):

        for i in range(5):
            text, response = self.posts(i)

            nodes = response.xpath('//table[@class="list_2_tab"]/tr')
            column_name = ['case_number', 'person_name', 'sex', 'age', 'identify_number', 'enterprise_name', 'area',
                           'executed_court', 'executed_number', 'executed_unit',
                           'execution', 'execution_detail', 'executed_item', 'not_execute', 'case_date', 'release_date']

            for node in nodes[1:]:
                d = {}
                url = 'http://www.hljcredit.gov.cn/' + node.xpath('.//td[2]/a/@href')[0].strip()
                print(url)
                # content = self._gets(url)
                # tree = etree.HTML(content)
                # item_list = tree.xpath('//table[@class="for_letter"]/tr')
                # for index, value in enumerate(column_name):
                #     d[value] = item_list[index].xpath('.//td[2]/text()')[0].strip()
                # doc.insert(d)

    def forbiden(self, text):
        re.findall('')


def main():
    spider = Spider()
    spider.loop()


if __name__ == '__main__':
    main()
