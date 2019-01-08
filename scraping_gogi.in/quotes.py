# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['gogi.in']
    start_urls = ['https://www.gogi.in/']

    def parse(self, response):
        self.log('I just Visited ' + response.url)
        for title in response.css('div.main-container'):
            item = {
                    'title' : title.css('h2.title.front-view-title > a::text').extract()
            }
            yield item

        next_page = response.css('a.next.page-numbers::attr(href)').extract_first()
        next_page = response.urljoin(next_page)
        yield scrapy.Request(url = next_page, callback = self.parse)