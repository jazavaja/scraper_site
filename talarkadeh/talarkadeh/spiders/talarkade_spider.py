import scrapy


class TalarkadeSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['https://example.com/articles']

    def parse(self, response):
        # استخراج عنوان مقاله‌ها از صفحه
        for article in response.css('div.article'):
            yield {
                'title': article.css('h2.title::text').get(),
                'url': article.css('a::attr(href)').get(),
            }

        # صفحه بعدی
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
