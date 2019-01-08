import scrapy


class Gsmarena(scrapy.Spider):
    name = 'gsm-review'
    allowed_domains = ['gsmarena.com']
    start_urls = ['https://www.gsmarena.com/reviews.php3']

    def parse(self, response):
        title_url = response.css('h3.review-item-title >a ::attr(href)').extract()
        for url in title_url:
            url = response.urljoin(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)




        next_page = response.css('a.pages-next::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url = next_page, callback = self.parse)

    def parse_detail(self, response):
        yield {
                'Model'  : response.css('li.article-info-meta-link.meta-link-specs > a ::text').extract_first(),
                'title'  : response.css('h1.article-info-name::text').extract_first(),
                'rate'   : response.css('span.score::text').extract_first(),
                'tags'   : response.css('p.float-right>a ::text').extract(),
                'company': response.css('p.float-right>a ::text').extract_first(),
                'Images' : response.css('img.inline-image::attr(src)').extract()
        }
        