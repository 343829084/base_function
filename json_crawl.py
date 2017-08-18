# -*-coding=utf-8-*-
import requests, urllib2, urllib, json


def using_requests():
    post_data = {'first': 'true', 'kd': 'Android', 'pn': '1'}
    url = "http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
    r = requests.post(url, data=post_data)
    #r=requests.post("http://www.lagou.com/jobs/positionAjax.json?px=default",data=post_data)
    print r.text


def getJson():
    user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    headers = {"User-Agent": user_agent}
    url = "http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"

    data = {"first": "false", "pn": "2", "kd": "Python"}
    post_data = urllib.urlencode(data)
    req = urllib2.Request(url, headers=headers, data=post_data)

    resp = urllib2.urlopen(req)
    return_data = resp.read()
    print return_data.decode("utf-8")
    f = open("json.txt", 'w')
    f.write(return_data)
    f.close()
    json_data = json.loads(return_data)
    print type(json_data)
    #print json_data['success']
    #print json

#using_requests()


def jsonParse(dictionary):
        if isinstance(dictionary,dict):
            for i in range(len(dictionary)):
                key=dictionary.keys()[i]
                value=dictionary[key]
                print key,value

                jsonParse(value)


def list_all_dict(dict_a):
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型

        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]

            temp_value = dict_a[temp_key]

            print"%s : %s" % (temp_key, temp_value)

            list_all_dict(temp_value)  # 自我调用实现无限遍历

def testcase1():
    new_url = 'http://api.k.sohu.com/api/channel/v6/news.go?p1=NjMwMjg4NTczMDc1OTEyNzA2OA%3D%3D&pid=-1&channelId=1&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=22.553053&cdma_lng=113.902393&from=channel&mac=b4%3A0b%3A44%3A83%3A93%3A16&AndroidID=4dd00e258bbe295f&carrier=CMCC&imei=990006203070023&imsi=460020242631842&density=3.0&apiVersion=37&skd=9bf84c6c9d24711f43f7058db2d1ed5ba7c6a2fecca504d3f44839a8bf22b4521ff192a4ac2d77946d871706ceb89baa269d145d2f5a07fddb656d6417029bb04459d2a5aa0ca50764b2de62da32f9e5e6055efa78b93cafbd89ef0971a836d3542ce2065edff7017a28b164e4210fec&v=1502985600&t=1503044087&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=440300&forceRefresh=0&apiVersion=37&u=1&source=0&isSupportRedPacket=0&t=1503044087'

    s=requests.get(new_url)
    js=s.json()
    #print js
    list_all_dict(js)

#getJson()
testcase1()
