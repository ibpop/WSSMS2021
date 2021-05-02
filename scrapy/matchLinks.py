# -*- coding: utf-8 -*-
import scrapy

upperLimitFlag = True

class Link(scrapy.Item):
    link = scrapy.Field()

class MatchlinksSpider(scrapy.Spider):
    name = 'matchLinks'
    allowed_domains = ['footballcritic.com']
    start_urls = ['https://www.footballcritic.com/premier-league/season-2019-2020/matches/2/21558']

    def parse(self, response):
        myXpath = '//ul[@class="info-list allMatches"]/child::span/child::li/a[1]/@href'
        
        links = response.xpath(myXpath)
        
        if upperLimitFlag:
            if len(links) > 100:
                links = links[0:100]                     
        
        for ll in links:
            l = Link()
            l['link'] = ll.get()
            yield l
