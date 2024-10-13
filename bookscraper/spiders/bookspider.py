import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_page = book.css('h3 a::attr(href)').get()

            if book_page is not None:
                if 'catalogue' in book_page:
                    book_page_url = 'https://books.toscrape.com/' + book_page
                else:
                    book_page_url = 'https://books.toscrape.com/catalogue/' + book_page
                yield response.follow(book_page_url, callback=self.parse_book_page)

            yield {
                'name': book.css('h3 a::attr(title)').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a::attr(href)').get()
            }

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css('table tr')

        yield {
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css('td::text').get(),
            'price_excl_tax': table_rows[2].css('td::text').get(),
            'price_incl_tax': table_rows[3].css('td::text').get(),
            'tax': table_rows[4].css('td::text').get(),
            'availability': table_rows[5].css('td::text').get(),
            'num_reviews': table_rows[6].css('td::text').get(),
            'stars': response.css('p.star-rating::attr(class)').get().split(' ')[-1],
            'category': response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get(),
            'description': response.xpath('//*[@id="content_inner"]/article/p/text()').get(),
            'price': response.css('p.price_color::text').get(),
        }

