import scrapy


class ScrapeRentItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    pictures = scrapy.Field()
    rent_price = scrapy.Field()
    description = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()
