import scrapy
from scrape_rent.items import ScrapeRentItem
import logging
import re

class KelmSpider(scrapy.Spider):
    name = 'kelm'
    allowed_domains = ['kelm-immobilien.de']
    start_urls = ['https://kelm-immobilien.de/immobilien/']

    def parse(self, response):
        self.log(f'Parsing main page: {response.url}', level=logging.INFO)
        rental_links = response.css('h3.property-title a::attr(href)').getall()
        self.log(f'Found rental links: {rental_links}', level=logging.INFO)
        if not rental_links:
            self.log('No rental links found. Check the CSS selector.', level=logging.ERROR)
        for href in rental_links:
            self.log(f'Following link: {href}', level=logging.INFO)
            yield response.follow(href, self.parse_rental)

    def parse_rental(self, response):
        self.log(f'Parsing rental page: {response.url}', level=logging.INFO)
        item = ScrapeRentItem()
        item['url'] = response.url
        item['title'] = response.css('h1.property-title::text').get().encode('latin-1', errors='ignore').decode('latin-1')
        self.log(f'Title: {item["title"]}', level=logging.INFO)
        item['status'] = response.css('div.dd.col-sm-7::text').get()
        self.log(f'Status: {item["status"]}', level=logging.INFO)
        

        rent_prices = response.css('div.dd.col-sm-7::text').getall()
        if rent_prices:
            last_price = rent_prices[-1].strip().encode('latin-1', errors='ignore').decode('latin-1')
            item['rent_price'] = last_price
        else:
            item['rent_price'] = None
        
        desc = response.css('div.property-description.panel.panel-default *::text').getall()
        clean_desc = [text.strip().encode('latin-1', errors='ignore').decode('latin-1') for text in desc if text.strip() and 'function' not in text]
        description = ' '.join(clean_desc).encode('latin-1', errors='ignore').decode('latin-1')

        description = re.sub(r'\{.*?\}', '', description)
        description = re.sub(r'\(.*?\)', '', description)
        item['description'] = description.strip()

        phone_text = response.css('div.dd.col-sm-7.p-tel.value a::attr(href)').getall()
        phone_number = None
        if phone_text:
            phone_text = ''.join(phone_text)
            if phone_text.startswith('+'):
                phone_number = phone_text
            else:
                phone_match = re.search(r'\+[\d\s-]+', phone_text)
                if phone_match:
                    phone_number = phone_match.group()
        item['phone_number'] = phone_number

        item['email'] = response.css('div.dd.col-sm-7.u-email.value a::attr(href)').re_first(r'mailto:(.*)')
        self.log(f'Email: {item["email"]}', level=logging.INFO)
        yield item
