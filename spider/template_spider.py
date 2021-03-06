# -*-coding=utf-8-*-
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


class Spider(object):

    def __init__(self):
        self.url = 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc='
        self.headers = {
                        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:39.0) Gecko/20100101 Firefox/39.0",
                        'Referer': 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gongchecklists'
                        }

        self.post_header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:39.0) Gecko/20100101 Firefox/39.0",
        }

        self.session = requests.Session()
        origin_url = 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=&proselect=&cityselect=&disselect='
        # r0=self.session.get(origin_url, headers=self.headers, proxies=get_proxy())
        r0 = self.session.get(origin_url, headers=self.headers, proxies=get_proxy())
        print('Cookie::{}'.format(r0.cookies))

    def gets(self):
        r = self.session.get(self.url, headers=self.headers, proxies=get_proxy())
        # r = self.session.get(self.url, headers=self.headers, proxies=get_proxy())
        print('Cookie::{}'.format(r.cookies))

        # js= json.loads(r.text)
        # print(r.text)
        tree = etree.HTML(r.text)
        return r.text, tree

    def _gets(self, url):
        # r = self.session.get(url, headers=self.headers, proxies=get_proxy())
        r = self.session.get(url, headers=self.headers, proxies=get_proxy())
        return r.text

    def posts(self, page):
        post_data = {'proselect': "", 'cityselect': "", 'disselect': "", 'curPageNO': str(page)}
        r = self.session.post(self.url, headers=self.headers, data=post_data, proxies=get_proxy())
        text = r.text
        tree = etree.HTML(r.text)
        return text, tree

    def download(self):
        r = requests.get(self.url)
        filename = 'code.png'
        with open(filename, 'wb') as f:
            f.write(r.content)

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
                content = self._gets(url)
                tree = etree.HTML(content)
                item_list = tree.xpath('//table[@class="for_letter"]/tr')
                for index, value in enumerate(column_name):
                    d[value] = item_list[index].xpath('.//td[2]/text()')[0].strip()
                doc.insert(d)


def main():
    spider = Spider()
    spider.parse()


if __name__ == '__main__':
    main()
