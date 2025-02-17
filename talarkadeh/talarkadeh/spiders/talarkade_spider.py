import scrapy

class TalarkadehSpider(scrapy.Spider):
    name = "talarkadeh"

    def __init__(self, url, whereSave, untilPage, *args, **kwargs):
        super(TalarkadehSpider, self).__init__(*args, **kwargs)
        self.url = url
        self.whereSave = whereSave
        self.untilPage = int(untilPage)
        self.start_urls = [url]

    def parse(self, response):
        links = response.css('a.card__title::attr(href)').getall()
        full_links = [response.urljoin(link) for link in links]

        # ذخیره کردن داده‌ها در فایل
        with open(self.whereSave, "a", encoding="utf-8") as f:
            for url in full_links:
                f.write(url + "\n")

        # پیدا کردن صفحه بعدی
        current_page = int(response.url.split("/")[-1]) if "page" in response.url else 1
        if current_page < self.untilPage:
            next_page = f"{self.url}/page/{current_page + 1}"
            yield scrapy.Request(next_page, callback=self.parse)

