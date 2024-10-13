# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from bookscraper.items import BookItem

class BookItemPipeline:
    def process_item(self, item, spider):
        ## Only for BookItem
        if not isinstance(item, BookItem):
            return item
        
        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name != 'description':
                adapter[field_name] = value[0].strip()
            else:
                adapter[field_name] = value[0]


        ## Category & Product Type => switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
        
        ## Price => convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ## Availability => extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        ## Num Reviews => convert to int
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        ## Stars => convert to int
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == 'four':
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5
        else:
            adapter['stars'] = -1

        return item


import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class SaveToMySQLPipeline:
    def __init__(self):
        ## Connect to MySQL
        self.conn = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_DATABASE')
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books(
                id INT PRIMARY KEY AUTO_INCREMENT,
                url VARCHAR(255),
                title text,
                upc VARCHAR(255),
                product_type VARCHAR(255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                price DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                category VARCHAR(255),
                description text
            )
        """)

    def process_item(self, item, spider):
        ## Only for BookItem
        if isinstance(item, BookItem):
            self.save_book_item(item)
        
        return item
        
    def save_book_item(self, item):
        ## Insert item into MySQL
        self.cur.execute("""
            INSERT INTO books (
                url,
                title,
                upc,
                product_type,
                price_excl_tax,
                price_incl_tax,
                tax,
                price,
                availability,
                num_reviews,
                stars,
                category,
                description
            ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['url'],
            item['title'],
            item['upc'],
            item['product_type'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['tax'],
            item['price'],
            item['availability'],
            item['num_reviews'],
            item['stars'],
            item['category'],
            item['description']
        ))

        # Execute inser of data into database
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        # Close cursor and connection to database
        self.cur.close()
        self.conn.close()
