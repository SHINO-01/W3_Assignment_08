import scrapy

class HotelScrapperItem(scrapy.Item):
    city = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
