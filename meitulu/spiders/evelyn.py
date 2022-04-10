import scrapy
from meitulu.items import Image

class Spider(scrapy.Spider):
    name = 'evelyn'
    # start_urls = ['http://meitulu.cn/t/Evelynaili/']

    def __init__(self, albumUrl=None, *args, **kwargs):
        if albumUrl == None:
            raise Exception('usage: -a albumUrl=...')

        super(Spider, self).__init__(*args, **kwargs)
        self.start_url = albumUrl

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        urls = response.css('div.main div.boxs ul.img li>a::attr(href)').extract()
        albumUrls = list(map(lambda url: response.urljoin(url), urls))
        names = response.css('div.main div.boxs ul.img li p.p_title> a::text').extract()

        for (albumUrl, name) in zip(albumUrls, names):
            yield scrapy.Request(
                url=albumUrl,
                callback=self.parseAlbum,
                cb_kwargs=dict(firstUrl=albumUrl, albumName=name, count=1))

    def parseAlbum(self, response, firstUrl, albumName, count):
        url = response.css('div.content center a img.content_img::attr(src)').extract_first()
        name = str(count) + '.jpg'
        
        yield Image(url=url, name=name, albumName=albumName, fromUrl=response.url)

        nextPage = response.urljoin(response.css('div.content center a::attr(href)').extract_first())
        if nextPage != firstUrl:
            yield scrapy.Request(
                url=nextPage,
                callback=self.parseAlbum,
                cb_kwargs=dict(firstUrl=nextPage, albumName=albumName, count=count+1))
        