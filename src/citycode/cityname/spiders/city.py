import scrapy

from cityname.items import CityItem
# spider to crawl city names and their respective codes from expedia.co.in
class LinkSpider(scrapy.Spider):
    name = "city"
    allowed_domains = ["expedia.co.in"]
    start_urls = [
        "http://www.expedia.co.in/Destinations-In-India.d80.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p2.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p3.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p4.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p5.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p6.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p7.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p8.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p9.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p10.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p11.Hotel-Destinations",
        "http://www.expedia.co.in/Destinations-In-India.d80-p12.Hotel-Destinations"
          
    ]

    def parse(self, response):
        for sel in response.xpath('//ul[@id="AllCityDestACol"]/li'):
            item = CityItem()
            temp = sel.xpath('a/@href').extract()[0]
            item['city'] = temp.split('.')[0].replace('-',' ').rsplit(' ',1)[0][1:]
            item['code'] = temp.split('.')[-2]
            yield item
        for sel in response.xpath('//ul[@id="AllCityDestBCol"]/li'):
            item = CityItem()
            temp = sel.xpath('a/@href').extract()[0]
            item['city'] = temp.split('.')[0].replace('-',' ').rsplit(' ',1)[0][1:]
            item['code'] = temp.split('.')[-2]
            yield item