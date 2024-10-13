import scrapy
from bookscraper.items import BookItem
#import random

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'booksdata.json': {'format': 'json', 'overwrite': True}
        }
    }

    # user_agent_list = [
    #     'Mozilla/5.0 (Linux x86_64) Gecko/20100101 Firefox/50.4',
    #     'Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/48.0.2228.310 Safari/600',
    #     'Mozilla/5.0 (Windows; Windows NT 6.3; Win64; x64) AppleWebKit/600.46 (KHTML, like Gecko) Chrome/52.0.3512.380 Safari/601',
    #     'Mozilla/5.0 (Android; Android 4.3.1; HUAWEI G6-L10 Build/HuaweiG6-L11) AppleWebKit/600.21 (KHTML, like Gecko)  Chrome/50.0.3862.278 Mobile Safari/536.2',
    #     'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_3; like Mac OS X) AppleWebKit/603.4 (KHTML, like Gecko)  Chrome/51.0.3158.350 Mobile Safari/603.5'
    # ]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_page = book.css('h3 a::attr(href)').get()

            if book_page is not None:
                if 'catalogue' in book_page:
                    book_page_url = 'https://books.toscrape.com/' + book_page
                else:
                    book_page_url = 'https://books.toscrape.com/catalogue/' + book_page
                yield response.follow(
                    book_page_url, 
                    callback=self.parse_book_page, 
                    #headers={'User-Agent': random.randint(0, len(self.user_agent_list) - 1)}
                )

            # yield {
            #     'name': book.css('h3 a::attr(title)').get(),
            #     'price': book.css('.product_price .price_color::text').get(),
            #     'url': book.css('h3 a::attr(href)').get()
            # }

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(
                next_page_url, 
                callback=self.parse,
                #headers={'User-Agent': random.randint(0, len(self.user_agent_list) - 1)}
            )

    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        book_item = BookItem()

        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css('td::text').get(),
        book_item['product_type'] = table_rows[1].css('td::text').get(),
        book_item['price_excl_tax'] = table_rows[2].css('td::text').get(),
        book_item['price_incl_tax'] = table_rows[3].css('td::text').get(),
        book_item['tax'] = table_rows[4].css('td::text').get(),
        book_item['availability'] = table_rows[5].css('td::text').get(),
        book_item['num_reviews'] = table_rows[6].css('td::text').get(),
        book_item['stars'] = response.css('p.star-rating::attr(class)').get(),
        book_item['category'] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get(),
        book_item['description'] = response.xpath('//*[@id="content_inner"]/article/p/text()').get(),
        book_item['price'] = response.css('p.price_color::text').get(),

        yield book_item

