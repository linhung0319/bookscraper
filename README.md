# BookScraper

BookScraper is a Scrapy project designed to scrape book information from the website [books.toscrape.com](https://books.toscrape.com). This project demonstrates various Scrapy features, including custom item pipelines, middleware for rotating user agents and proxies, and database integration.

## Project Structure

```
bookscraper/
│
├── bookscraper/
│   ├── spiders/
│   │   └── bookspider.py
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   └── settings.py
│
├── .env
└── README.md
```

## Features

- Scrapes book details including title, price, availability, and more
- Custom item pipeline for data cleaning and processing
- Fake User-Agent rotation using ScrapeOps API
- Proxy rotation using scrapy-rotating-proxies
- Option to save data to MySQL database

## Prerequisites

- Python 3.x
- Scrapy
- MySQL (optional, for database storage)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bookscraper.git
   cd bookscraper
   ```

2. Install the required packages:
   ```
   pip install scrapy mysql-connector-python python-dotenv requests scrapy-rotating-proxies
   ```

3. Set up your environment variables by creating a `.env` file in the project root:
   ```
   DB_HOST=your_db_host
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_DATABASE=your_db_name
   SCRAPEOPS_API_KEY=your_scrapeops_api_key
   ```

## Usage

To run the spider:

```
scrapy crawl bookspider
```

This will start the scraping process and save the results to `booksdata.json` in the project root.

## Configuration

You can modify the following settings in `settings.py`:

- `SCRAPEOPS_FAKE_USER_AGENTS_ACTIVE`: Enable/disable fake user agent rotation
- `SCRAPEOPS_NUM_RESULTS`: Number of fake user agents to fetch
- `ROTATING_PROXY_LIST`: List of proxy servers to use
- `ITEM_PIPELINES`: Enable/disable specific item pipelines

### Rotating Proxies

This project uses the `scrapy-rotating-proxies` package for proxy rotation. To set it up:

1. Install the package: `pip install scrapy-rotating-proxies`
2. Add the following to your `settings.py`:

   ```python
   ROTATING_PROXY_LIST = [
       'proxy1.com:8000',
       'proxy2.com:8031',
       # Add more proxies here
   ]

   DOWNLOADER_MIDDLEWARES = {
       # ...
       'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
       'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
   }
   ```

Note: While using free proxies, you may encounter issues such as slow response times, non-functioning proxies, or proxies that have been blacklisted. For more reliable scraping, consider using paid proxy services.

## Data Storage

By default, the scraped data is saved to a JSON file. To enable MySQL storage:

1. Uncomment the `SaveToMySQLPipeline` in `ITEM_PIPELINES` in `settings.py`
2. Ensure your MySQL credentials are correctly set in the `.env` file

## Customization

- To modify the scraping behavior, edit `bookspider.py` in the `spiders` directory
- To change data processing logic, modify the pipelines in `pipelines.py`
- To adjust middleware behavior, edit `middlewares.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
