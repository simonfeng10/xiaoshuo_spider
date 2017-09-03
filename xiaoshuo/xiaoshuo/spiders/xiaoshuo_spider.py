import scrapy
import re

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    start_urls = ['http://r.qidian.com/yuepiao?chn=-1']

    def parse(self, response):
        book_name = response.xpath('//div[@class="book-mid-info"]/h4/a/text()').extract()
        # urls = response.xpath('//div[@class="book-mid-info"]/h4/a/@href').extract()[0]
        # yield scrapy.Request(url = response.urljoin(urls), callback = self.parse_detail)
        urls = response.xpath('//div[@class="book-mid-info"]/h4/a/@href').extract()
        for curr_url in urls:
            yield scrapy.Request(url = response.urljoin(curr_url), callback = self.parse_detail)

    def parse_detail(self, response):
        urls_detail = response.xpath('//li[@class="j_discussion_block"]/a/@href').extract()[0]
        yield scrapy.Request(url = response.urljoin(urls_detail), callback = self.parse_discussion)

    def parse_discussion(self, response):
        # id = response.xpath('//p[@class="post-auther"]/a/text()').extract()
        # item['name'] = response.xpath('//div[@class="main-header"]/h1/a/text()').extract()
        # for i in range(len(id)):
        #     item['id'] = response.xpath('//p[@class="post-auther"]/a/text()').extract()[i]
        #     item['discussion'] = response.xpath('//p[@class="post-body"]/a/text()').extract()[i]
        #     yield item
        #造成 id 和 discussion 不匹配
        current_url = response.url
        if current_url.find('page') == -1:
            current_url = current_url + '?type=1&page=1'

        position = current_url.find('page')
        name = response.xpath('//div[@class="main-header"]/h1/a/text()').extract()[0]
        current_page = re.findall(r"(?<=page\=).*", current_url)[0]
        sites = response.xpath('//li[@class="post-wrap"]')
        for site in sites:
            item = {}
            item['name'] = name
            item['current_url'] = current_url
            item['current_page'] = current_page
            item['id'] = site.xpath('div[@class="post"]/p[@class="post-auther"]/a/text()').extract()[0]
            item['discussion'] = site.xpath('div[@class="post"]/p[@class="post-body"]/a/text()').extract()[0]
            yield item

        for i in range(2, 11):
            standard_url = current_url[:position+5]
            yield scrapy.Request(url = standard_url + str(i), callback = self.parse_discussion)
        # next_url = response.xpath('//li[@class="lbf-pagination-item"]/a[@class="lbf-pagination-next"]/@href').extract()
        # if next_url:
            # yield scrapy.Request(url = next_url, callback = sef.parse_discussion)
