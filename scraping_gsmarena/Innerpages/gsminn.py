import scrapy


class Gsmarena(scrapy.Spider):
    name = 'gsm-review'
    allowed_domains = ['gsmarena.com']
    start_urls = ['https://www.gsmarena.com/reviews.php3']

    def parse(self, response):
        title_url = response.css('h3.review-item-title >a ::attr(href)').extract()
        for url in title_url:
            url = response.urljoin(url)
            yield scrapy.Request(url= url, callback= self.parse_inner)

    def parse_inner(self, response):
        next_review_page = response.css('a.pages-next::attr(title)').extract_first()
        if next_page:
            next_review_page = response.urljoin(next_review_page)
            yield scrapy.Request(url= next_review_page, callback= self.parse_images)


        next_page = response.css('a.pages-next::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url = next_page, callback = self.parse)


    def parse_images(self, response):
        yield{
        'Images' : response.css('img.inline-image::attr(src)').extract()
        }

  
    