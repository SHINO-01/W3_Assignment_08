BOT_NAME = "hotel_scrapper"

SPIDER_MODULES = ["hotel_scrapper.spiders"]
NEWSPIDER_MODULE = "hotel_scrapper.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2

# Configure the Images Pipeline
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    "hotel_scrapper.pipelines.HotelScrapperPipeline": 300,  # Keep your custom pipeline for database storage
}

# Folder to store downloaded images
IMAGES_STORE = 'media/images'

# Allow redirected responses for image URLs
MEDIA_ALLOW_REDIRECTS = True

# Handle HTTP error codes
HTTPERROR_ALLOW_ALL = True  # Handle redirects if necessary


LOG_LEVEL = 'INFO'
FEED_EXPORT_ENCODING = "utf-8"

DATABASE = {
    'drivername': 'postgresql',
    'host': 'postgres',
    'port': '5432',
    'username': 'scrapy_user',
    'password': 'scrapy_pass',
    'database': 'scrapyDB',
}
