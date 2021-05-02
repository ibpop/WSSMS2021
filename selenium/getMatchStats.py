from selenium import webdriver
import time
import pandas as pd

upperLimitFlag = True

gecko_path = '/home/bpop/bin/geckodriver'

url = 'https://www.footballcritic.com/premier-league/season-2019-2020/matches/2/21558'

options = webdriver.firefox.options.Options()
options.headless = True

driver = webdriver.Firefox(options = options, executable_path = gecko_path)

driver.get(url)

# Get links to match webpages
matchLinksXpath = '//ul[@class="info-list allMatches"]/child::span/child::li/a[1]'

matchLinks = []

for link in driver.find_elements_by_xpath(matchLinksXpath):
    if upperLimitFlag:
        if len(matchLinks) > 99:
            break
    matchLinks.append(link.get_attribute('href'))
    
# Get stats for each match
stats = pd.DataFrame({'MatchDate':[], 'Week':[], 'HomeTeam':[], 'AwayTeam':[], \
                      'HomeGoalsHT':[], 'AwayGoalsHT':[], \
                      'HomeGoalsFT':[], 'AwayGoalsFT':[], \
                      'HomeBallPos':[], 'AwayBallPos':[], \
                      'HomeShotsOffTarget':[], 'AwayShotsOffTarget':[], \
                      'HomeShotsOnTarget':[], 'AwayShotsOnTarget':[], \
                      'HomeCorners':[], 'AwayCorners':[], \
                      'HomeFouls':[], 'AwayFouls':[], \
                      'HomeYellowCards':[], 'AwayYellowCards':[], \
                      'HomeRedCards':[], 'AwayRedCards':[], \
                      })

for link in matchLinks:
    driver.get(link)
    
    dateXpath = '//span[@data-type="date_1"]'
    matchDate = driver.find_element_by_xpath(dateXpath).text
    
    weekXpath = '//div[@class="header_matchblock"]/child::b'
    # Ommit first 23 signs ("Premier League Gameweek
    week = driver.find_element_by_xpath(weekXpath).text[24:]
    
    teamNamesXpath = '//strong[@class="name"]/a'
    homeTeam = driver.find_elements_by_xpath(teamNamesXpath)[0].text
    awayTeam = driver.find_elements_by_xpath(teamNamesXpath)[1].text
    
    goalsXpath = '//ul[@class="add-info"]/li/span'
    homeGoalsHT = driver.find_elements_by_xpath(goalsXpath)[0].text.split('-')[0]
    awayGoalsHT = driver.find_elements_by_xpath(goalsXpath)[0].text.split('-')[1]
    homeGoalsFT = driver.find_elements_by_xpath(goalsXpath)[1].text.split('-')[0]
    awayGoalsFT = driver.find_elements_by_xpath(goalsXpath)[1].text.split('-')[1]
    
    # Get stats block for further use
    statsBlockXpath = '//div[@class="stats-block"]/descendant::'
    
    ballPosXpath = statsBlockXpath+'strong[@class="points"]'
    homeBallPos = driver.find_elements_by_xpath(ballPosXpath)[0].text
    awayBallPos = driver.find_elements_by_xpath(ballPosXpath)[1].text
    
    homeShotsXpath = statsBlockXpath+'div[@class="side-one"]/child::span[@class="num"]'
    homeShotsOffTarget = driver.find_elements_by_xpath(homeShotsXpath)[0].text
    homeShotsOnTarget = driver.find_elements_by_xpath(homeShotsXpath)[1].text
    
    awayShotsXpath = statsBlockXpath+'div[@class="side-two"]/child::span[@class="num"]'
    awayShotsOffTarget = driver.find_elements_by_xpath(awayShotsXpath)[0].text
    awayShotsOnTarget = driver.find_elements_by_xpath(awayShotsXpath)[1].text
    
    cornersXpath = statsBlockXpath+'strong[contains(text(), "Corners")]/following-sibling::span'
    homeCorners = driver.find_elements_by_xpath(cornersXpath)[0].text
    awayCorners = driver.find_elements_by_xpath(cornersXpath)[1].text
    
    foulsXpath = statsBlockXpath+'strong[contains(text(), "Fouls")]/following-sibling::span'
    homeFouls = driver.find_elements_by_xpath(foulsXpath)[0].text
    awayFouls = driver.find_elements_by_xpath(foulsXpath)[1].text
    
    yellowCardsXpath = statsBlockXpath+'strong[contains(text(), "Yellow cards")]/following-sibling::span'
    homeYellowCards = driver.find_elements_by_xpath(yellowCardsXpath)[0].text
    awayYellowCards = driver.find_elements_by_xpath(yellowCardsXpath)[1].text
    
    redCardsXpath = statsBlockXpath+'strong[contains(text(), "Red cards")]/following-sibling::span'
    homeRedCards = driver.find_elements_by_xpath(redCardsXpath)[0].text
    awayRedCards = driver.find_elements_by_xpath(redCardsXpath)[1].text
    
    match = {'MatchDate':matchDate, 'Week':week, 'HomeTeam':homeTeam, 'AwayTeam':awayTeam, \
         'HomeGoalsHT':homeGoalsHT, 'AwayGoalsHT':awayGoalsHT, \
         'HomeGoalsFT':homeGoalsFT, 'AwayGoalsFT':awayGoalsFT, \
         'HomeBallPos':homeBallPos, 'AwayBallPos':awayBallPos, \
         'HomeShotsOffTarget':homeShotsOffTarget, 'AwayShotsOffTarget':awayShotsOffTarget, \
         'HomeShotsOnTarget':homeShotsOnTarget, 'AwayShotsOnTarget':awayShotsOnTarget, \
         'HomeCorners':homeCorners, 'AwayCorners':awayCorners, \
         'HomeFouls':homeFouls, 'AwayFouls':awayFouls, \
         'HomeYellowCards':homeYellowCards, 'AwayYellowCards':awayYellowCards, \
         'HomeRedCards':homeRedCards, 'AwayRedCards':awayRedCards, \
         }
    stats = stats.append(match, ignore_index=True)
    
# stats.to_json('matchesStats.json')
stats.to_csv('matchesStats.csv')

#time.sleep(30)

# Close browser:
driver.quit()
