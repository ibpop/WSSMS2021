# -*- coding: utf-8 -*-
import scrapy

class MatchStats(scrapy.Item):
    MatchDate = scrapy.Field()
    Week = scrapy.Field()
    HomeTeam = scrapy.Field()
    AwayTeam = scrapy.Field()
    HomeGoalsHT = scrapy.Field()
    AwayGoalsHT = scrapy.Field()
    HomeGoalsFT = scrapy.Field()
    AwayGoalsFT = scrapy.Field()
    HomeBallPos = scrapy.Field()
    AwayBallPos = scrapy.Field()
    HomeShotsOffTarget = scrapy.Field()
    AwayShotsOffTarget = scrapy.Field()
    HomeShotsOnTarget = scrapy.Field()
    AwayShotsOnTarget = scrapy.Field()
    HomeCorners = scrapy.Field()
    AwayCorners = scrapy.Field()
    HomeFouls = scrapy.Field()
    AwayFouls = scrapy.Field()
    HomeYellowCards = scrapy.Field()
    AwayYellowCards = scrapy.Field()
    HomeRedCards = scrapy.Field()
    AwayRedCards = scrapy.Field()

class GetstatsSpider(scrapy.Spider):
    name = 'getStats'
    allowed_domains = ['footballcritic.com']
    try:
        with open("matchLinks.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        matchStats = MatchStats()
        
        dateXpath = '//span[@data-type="date_1"]/text()'
        matchStats['MatchDate'] = response.xpath(dateXpath).get()
        
        weekXpath = '//div[@class="header_matchblock"]/child::b/text()'
        # '\n' signs used for splitting the string (2nd is 'Gameweek xx')
        matchStats['Week'] = response.xpath(weekXpath).getall()[1].split('\n')[2][9:]
        
        teamNamesXpath = '//strong[@class="name"]/a/text()'
        matchStats['HomeTeam'] = response.xpath(teamNamesXpath).getall()[0]
        matchStats['AwayTeam'] = response.xpath(teamNamesXpath).getall()[1]
        
        goalsXpath = '//ul[@class="add-info"]/li/span/text()'
        matchStats['HomeGoalsHT'] = \
            response.xpath(goalsXpath)[0].get().strip().split('-')[0]
        matchStats['AwayGoalsHT'] = \
            response.xpath(goalsXpath)[0].get().strip().split('-')[1]
        
        matchStats['HomeGoalsFT'] = \
            response.xpath(goalsXpath)[1].get().strip().split('-')[0]
        matchStats['AwayGoalsFT'] = \
            response.xpath(goalsXpath)[1].get().strip().split('-')[1]
        
        # Get stats block for further use
        statsBlockXpath = '//div[@class="stats-block"]/descendant::'
        
        ballPosXpath = statsBlockXpath+'strong[@class="points"]/text()'
        matchStats['HomeBallPos'] = response.xpath(ballPosXpath)[0].get()
        matchStats['AwayBallPos'] = response.xpath(ballPosXpath)[1].get()
        
        homeShotsXpath = statsBlockXpath+'div[@class="side-one"]/child::span[@class="num"]/text()'
        matchStats['HomeShotsOffTarget'] = response.xpath(homeShotsXpath)[0].get()
        matchStats['HomeShotsOnTarget'] = response.xpath(homeShotsXpath)[1].get()
        
        awayShotsXpath = statsBlockXpath+'div[@class="side-two"]/child::span[@class="num"]/text()'
        matchStats['AwayShotsOffTarget'] = response.xpath(awayShotsXpath)[0].get()
        matchStats['AwayShotsOnTarget'] = response.xpath(awayShotsXpath)[1].get()
        
        cornersXpath = statsBlockXpath+'strong[contains(text(), "Corners")]/following-sibling::span/text()'
        matchStats['HomeCorners'] = response.xpath(cornersXpath)[0].get()
        matchStats['AwayCorners'] = response.xpath(cornersXpath)[1].get()
        
        foulsXpath = statsBlockXpath+'strong[contains(text(), "Fouls")]/following-sibling::span/text()'
        matchStats['HomeFouls'] = response.xpath(foulsXpath)[0].get()
        matchStats['AwayFouls'] = response.xpath(foulsXpath)[1].get()
        
        yellowCardsXpath = statsBlockXpath+'strong[contains(text(), "Yellow cards")]/following-sibling::span/text()'
        matchStats['HomeYellowCards'] = response.xpath(yellowCardsXpath)[0].get()
        matchStats['AwayYellowCards'] = response.xpath(yellowCardsXpath)[1].get()
        
        redCardsXpath = statsBlockXpath+'strong[contains(text(), "Red cards")]/following-sibling::span/text()'
        matchStats['HomeRedCards'] = response.xpath(redCardsXpath)[0].get()
        matchStats['AwayRedCards'] = response.xpath(redCardsXpath)[1].get()
                
        
        yield matchStats
