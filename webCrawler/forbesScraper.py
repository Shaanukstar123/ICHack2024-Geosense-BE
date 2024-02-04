import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
import logging

class ForbesSpider(CrawlSpider):
    name = 'forbes'
    allowed_domains = ['www.forbes.com']
    start_urls = ['https://www.forbes.com/']

    def __init__(self, *args, **kwargs):
        super(ForbesSpider, self).__init__(*args, **kwargs)
        self.item_id = 0 

    rules = (
        Rule(LinkExtractor(allow=r'/sites/.+2024/(01|02)/'), callback='parse_item', follow=True),
    )




    def parse_item(self, response):
        self.item_id += 1
        logging.info(f'Parsing URL: {response.url}')  # Added logging
        yield {
            'id': self.item_id, 
            'url': response.url,
            'title': response.css('title::text').get(),
            'content': ' '.join(response.css('div.article-body-container p::text').getall()).strip()
        }

def run_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
            },
        },
    })
    process.crawl(ForbesSpider)
    process.start()

if __name__ == '__main__':
    run_spider()
# replace