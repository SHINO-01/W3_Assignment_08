import os

BOT_NAME = "hotel_scrapper"

SPIDER_MODULES = ["hotel_scrapper.spiders"]
NEWSPIDER_MODULE = "hotel_scrapper.spiders"

ROBOTSTXT_OBEY = False  # Temporarily disabled for debugging
DOWNLOAD_DELAY = 1  # Reduced delay

# Configure the Images Pipeline
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    "hotel_scrapper.pipelines.HotelScrapperPipeline": 300,
}

# Folder to store downloaded images
IMAGES_STORE = 'media/images'

# Image pipeline settings
IMAGES_URLS_FIELD = 'image_urls'
IMAGES_RESULT_FIELD = 'images'

# Allow redirected responses for image URLs
MEDIA_ALLOW_REDIRECTS = True

# Handle HTTP error codes
HTTPERROR_ALLOW_ALL = True

# Logging configuration
LOG_LEVEL = 'DEBUG'
FEED_EXPORT_ENCODING = "utf-8"

# User-Agent to mimic a browser
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Retry configuration
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 404]

DATABASE = {
    'drivername': 'postgresql',
    'host': 'postgres',
    'port': '5432',
    'username': 'scrapy_user',
    'password': 'scrapy_pass',
    'database': 'scrapyDB',
}