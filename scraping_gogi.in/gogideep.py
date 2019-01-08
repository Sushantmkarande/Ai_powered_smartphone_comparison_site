import scrapy


class Gogideep(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['gogi.in']
    start_urls = ['https://www.gogi.in/']

    def parse(self, response):
        title_url = response.css('h2.title.front-view-title>a::attr(href)').extract()
        for url in title_url:
            url = response.urljoin(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)




        next_page = response.css('a.next.page-numbers::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url = next_page, callback = self.parse)

    def parse_detail(self, response):
        yield {
                'Model'  : response.css('h5.review-title::text').extract_first().strip(),
                'title'  : response.css('h1.title.single-title.entry-title::text').extract_first(),
                'rate'   : response.css('span.review-total-box::text').extract_first(),
                'content': response.css('div.thecontent>p::text').extract()
        }
        