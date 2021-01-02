import scrapy 
from Scraper.items import FirstScrapyItem
from scrapy.loader import ItemLoader     
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class firstSpider(CrawlSpider):
    name = 'crawler'

    allowed_domains = ['sellercentral.amazon.com']
    start_urls = ["https://sellercentral.amazon.com/forums/c/selling-on-amazon?no_subcategories=false","https://sellercentral.amazon.com/forums/c/selling-on-amazon?no_subcategories=false&page=1"]

    for x in range(2,4):
        url = "https://sellercentral.amazon.com/forums/c/selling-on-amazon?no_subcategories=false&page=" + str(x)
        start_urls.append(url)
    
    rules = [Rule(LinkExtractor(allow = '/forums/t/'), callback = 'parse_url', follow = True)]

    def parse_url(self, response):
        
        print()
        print("POST TITLE")
        print(response.xpath('//h1/a/text()').get())    #gives post title 
        title = response.xpath('//h1/a/text()').get()
       
        print("POST CATEGORIES")
        print(response.css('span[itemprop="title"]::text').getall())    #gives post categories
        categories = response.css('span[itemprop="title"]::text').getall()
       
        comments = []
        print("POST COMMENTS")   
        for post in response.css('div.post'): 
            for p in post.xpath('p/text()'):    
                print(p.extract())   
                comments.append(p.extract())
    
        yield {
            'title' : title,
            'categories' : categories,
            'comments' : comments,
        } 