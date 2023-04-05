import scrapy
from meitulu.items import Image
import re
class Spider(scrapy.Spider):
    name = 'evelyn'
    def __init__(self, album_url=None, *args, **kwargs):
        if album_url == None:
            raise Exception('usage: -a albumUrl=...')

        super(Spider, self).__init__(*args, **kwargs)
        self.start_url = album_url

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        # urls = response.css('div.main div.boxs ul.img li>a::attr(href)').extract()
        # albumUrls = list(map(lambda url: response.urljoin(url), urls))
        # names = response.css('div.main div.boxs ul.img li p.p_title> a::text').extract()

        urls = response.css("div.my-gutters-b div a::attr(href)").extract()
        album_urls = list(map(lambda url: response.urljoin(url), urls))
        names = response.css("div.my-gutters-b div a div.my-card-title::text").extract()

        for (album_url, name) in zip(album_urls, names):
            yield scrapy.Request(
                url=album_url,
                callback=self.parse_album,
                cb_kwargs=dict(album_name=name, count=1))

    def parse_album(self, response, album_name, count):
        urls = response.css("div.container-inner-fix-m img::attr(src)").extract()
        image_urls = list(map(lambda url: response.urljoin(url), urls))

        for url in image_urls:
            name = str(count) + ".jpg"
            yield Image(url=url, name=name, album_name=album_name, from_url=response.url)
            count += 1

        anchors = response.css("div.container ul.pagination li a.page-link").extract()
        pages = response.css("div.container ul.pagination li a.page-link::attr(href)").extract()

        next_page_anchor = anchors[-1]
        pattern = re.compile(r"href")

        if re.search(pattern, next_page_anchor) != None:
            next_page = response.urljoin(pages[-1])
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_album,
                cb_kwargs=dict(album_name=album_name, count=count+1))
        