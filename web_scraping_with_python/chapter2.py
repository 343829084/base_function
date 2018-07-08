import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue
import csv
import re
import urlparse
import lxml.html

def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1, scrape_callback=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = [seed_url]
    host_url='http://example.webscraping.com/'
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    # rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        # check url passes robots.txt restrictions
        if True:
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            print(len(html))
            # print(html)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
                print(links)

            if depth != max_depth:
                # can still crawl further
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(urlparse.urljoin(host_url,link) for link in get_links(html) if re.search(link_regex, link))
                    print(links)

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:', url)

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        print('in call')
        print(url)
        if re.search('/default/view', url) and (not re.search('(login|register)',url)):
            print('in search function')
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                print(field)
                details=tree.xpath('//table/tr[@id="places_{}__row"]/td[@class="w2p_fw"]/text()'.format(field))
                # print('details',details)
                # details=details[0].text_content()
                print(details)
                if details:
                    row.append(details[0])
            if row:
                self.writer.writerow(row)

class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
        
    def wait(self, url):
        """Delay if have accessed this domain recently
        """
        domain = urlparse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()



def download(url, headers, proxy, num_retries, data=None):
    print('Downloading:', url)
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print('Download error:', e.reason)
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                html = download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    return html


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp
        

def get_links(html):
    """Return a list of links from html 
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    result= webpage_regex.findall(html)
    print(result)
    return result

if __name__ == '__main__':
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

    # link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com/places/default/index/', 'default/view',user_agent=ua, scrape_callback=ScrapeCallback())