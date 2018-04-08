import scrapy
from image.items import pexelsItem
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class pexels(scrapy.spiders.Spider):
    """爬虫pexels"""
    name = 'pexels'

    # 减慢爬取速度为 3s
    #download_delay = 3

    allowed_domains = ['pexels.com'] # 允许爬取的域名

    start_urls = [
        # 起始url
        "https://www.pexels.com/?page=1",
    ]

    # cookies = {}
    # headers = {}
    # meta = {}

    # 初始化URL
    def __init__(self):
        super().__init__()
        # 多线程爬取主网页
        #for i in range(285, 1000):
        #    self.start_urls.append("https://www.pexels.com/?page=" + str(i))

    # 查询子网页
    def parse_item(self, response):
        item = response.meta['item']
        sel = scrapy.Selector(response)
        item['tags'] = sel.xpath('/html/body/div/div/section/div/div/ul/li/a/text()').extract()
        return item

    # 主网页
    def parse(self, response):
        self.logger.error('===============' + response.url + '===============')
        print('===============', response.url, '===============')

        # 解析子网页
        sel = scrapy.Selector(response)
        for each in sel.xpath('//article/a'):
            href = each.xpath('@href').extract()[0]
            title = each.xpath('img/@alt').extract()[0]
            src = each.xpath('img/@src').extract()[0].split('?')[0]
            # print("href:%s; title:%s; src:%s;" % (href, title, src))

            # 保存item
            item = pexelsItem()
            item['id'] = 0
            #item['url'] = response.urljoin(href)
            item['url'] = ('https://www.pexels.com' + href)
            item['title'] = title
            item['image_url'] = src

            # 查询子网页
            yield Request(item['url'], callback=self.parse_item, meta={'item': item, 'download_timeout': 30}, errback=self.errback_httpbin)
            # 如果不需要查询子网页就直接yield item

        # 递归下一个网页
        current_url = response.url.split('=')  # 爬取时请求的url
        num = int(current_url[-1]) + 1
        if num <= 3000:
            link = ''.join(current_url[:-1]) + '=' + str(num)
            # yield 不会直接中断当前函数
            yield Request(link, callback=self.parse, meta={'download_timeout': 30}, errback=self.errback_httpbin) # 超时30秒重连

    def errback_httpbin(self, failure):
        self.logger.error('swf-httpbin')
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('swf-HttpError on %s', response.url)
            return Request(response.url, callback=response.callback, meta=response.meta, errback=response.errback, dont_filter=True) # 重连

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('swf-DNSLookupError on %s', request.url)
            return Request(request.url, callback=request.callback, meta=request.meta, errback=request.errback, dont_filter=True) # 重连

        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('swf-TimeoutError on %s', request.url)
            return Request(request.url, callback=request.callback, meta=request.meta, errback=request.errback, dont_filter=True) # 超时重连

        elif failure.check(TCPTimedOutError):
            request = failure.request
            self.logger.error('swf-TCPTimedOutError on %s', request.url)
            return Request(request.url, callback=request.callback, meta=request.meta, errback=request.errback, dont_filter=True) # 超时重连
