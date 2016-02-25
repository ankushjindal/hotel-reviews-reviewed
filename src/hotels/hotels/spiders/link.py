import scrapy
from scrapy.http.request import Request
from hotels.items import LinkItem
# spider to crawl names of hotels and their reviews
class LinkSpider(scrapy.Spider):
    name = "link"
    getstr = raw_input('')
    codeS = getstr.split('_')[1]
    cityS = getstr.split('_')[0]
    cityST = cityS.replace('-','+')
    # url to collect the names of hotels of particular city 
    surl = "http://www.expedia.co.in/All-"+cityS+"-Hotels."+codeS+".Travel-Guide-City-All-Hotels"    
    start_urls = [surl]
    
    # function to collect names of hotels from expedia.co.in 
    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = LinkItem()
            item['title'] = sel.xpath('a[@class="normalText"]/text()').extract()
            if item['title']:
                item['title'] = item['title'][0]
                # url to search for particular hotel on holidayiq.com
                hiqSURL = "http://www.holidayiq.com/discovery/controllers/front_controller.php?_page=search&type=DESTINATION&query="+item['title'].replace(" ","+")+"+"+self.cityST
                request = scrapy.Request(hiqSURL, callback = self.parsehiqSearch)
                request.meta['item'] = item
                yield request

    # function to crawl the link of the particular hotel from holidayiq.com 
    def parsehiqSearch(self, response):
        item = response.meta['item']
        item['holidayiqU'] = response.xpath('//*[@id="search-block"]/div[1]/div/ul/li/h5/a/@href').extract()
        if item['holidayiqU']:
            item['holidayiqU'] = item['holidayiqU'][0]
            request2 = scrapy.Request(item['holidayiqU'], callback = self.parsehiqReview)
            request2.meta['item'] = item
            return request2

    # function to crawl the reviews of the hotel from holidayiq.com 
    def parsehiqReview(self, response):
        item =response.meta['item']
        item['holidayiqR'] = response.xpath('//blockquote[@class="margin0 review_datail_height"]/text()').extract()
        # url to search for particular hotel on tripadvisor
        taSURL = "http://www.tripadvisor.in/Search?q="+item['title'].replace(" ","+")+"+"+self.cityST
        request3 = scrapy.Request(taSURL, callback = self.parseTripSearch)
        request3.meta['item'] = item
        return request3 

    # function to crawl the link of the particular hotel from tripadvisor.in
    def parseTripSearch(self, response):
         item = response.meta['item']
         item['tripadvisorU'] = response.xpath('//*[@id="SEARCH_RESULTS"]/div[1]/div[1]/div[1]/a/@href').extract()
         if item['tripadvisorU']:
            item['tripadvisorU'] = item['tripadvisorU'][0]
            taRURL = "http://www.tripadvisor.in/"+item['tripadvisorU']
            request4 = scrapy.Request(taRURL, callback = self.parseTripReview)
            request4.meta['item'] = item
            return request4
    # function to crawl the reviews,amenities, location, price of the hotel from holidayiq.com 
    def parseTripReview(self, response):
        item = response.meta['item']
        loc1= response.xpath('//span[@class="street-address"]/text()').extract()
        loc2= response.xpath('//span[@class="extended-address"]/text()').extract()
        loc3= response.xpath('//span[@class="locality"]/text()').extract()
        loc4= response.xpath('//span[@property="v:locality"]/text()').extract()
        loc5= response.xpath('//span[@property="v:postal-code"]/text()').extract()
        loc6= response.xpath('//span[@class="country-name"]/text()').extract()
        l1 = loc1[0].strip() if loc1 else ''
        l2 = loc2[0].strip() if loc2 else ''
        l3 = loc3[0].strip() if loc3 else ''
        l4 = loc4[0].strip() if loc4 else ''
        l5 = loc5[0].strip() if loc5 else ''
        l6 = loc6[0].strip() if loc6 else ''
        lc1 = l1+', ' if l1 else ''
        lc2 = l2+', ' if l2 else ''
        lc3 = l3+', ' if l3 else ''
        lc4 = l4+' ' if l4 else ''
        lc5 = l5+', ' if l5 else ''
        lc6 = l6 if l6 else ''
        item['location'] = lc1+lc2+lc3+lc4+lc5+lc6
        item['stars'] = response.xpath('//div[@class="additional_info stars"]/text()').extract()
        item['price'] = response.xpath('//span[@property="v:pricerange"]/text()').extract()
        item['amenities'] =response.xpath('//ul[@class="property_tags"]/li/text()').extract()
        item['tripadvisorR'] = response.xpath('//p[@class="partial_entry"]/text()').extract()
        return item