import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import os
import json

class CrawlingAgent(CrawlSpider):
    name = "newsRound"
    allowed_domains = ["bloomberg.com"]
    start_urls = ["https://www.bloomberg.com/"]
    
    # Adjust the allow parameter to more specifically target article URLs
    rules = (
        Rule(LinkExtractor(allow=r'/articles/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # Check if the page is an article by looking for an article title
        article_name = response.xpath('//h1/text()').get() or response.css('h1::text').get()
        if article_name:
            article_content = ' '.join(response.xpath('//div[contains(@class, "body-copy")]//p/text()').getall() or response.css('div.body-copy p::text').getall())
            return {
                'name': article_name.strip(),
                'content': article_content.strip(),
                'url': response.url  # Including URL for reference
            }

def run_crawler():
    # Ensure the output directory exists
    output_dir = '../data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, 'output.json')
    if os.path.exists(output_file):
        os.remove(output_file)
    
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': output_file,
        'LOG_LEVEL': 'INFO',
        'CLOSESPIDER_ITEMCOUNT': 10
    })
    process.crawl(CrawlingAgent)
    process.start()

def fetch_news():
    run_crawler()
    try:
        with open('../data/output.json', 'r') as file:
            news_data = json.load(file)
        return news_data
    except FileNotFoundError:
        return {"error": "News data not found"}

if __name__ == "__main__":
    print(fetch_news())
