from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as BS
import pandas as pd

upperLimitFlag = True

# Premier League matches from season 2019-2020
req = Request('https://www.footballcritic.com/premier-league/season-2019-2020/matches/2/21558', \
              headers={'User-Agent':'Mozilla/5.0'} )
html = urlopen(req)
bs = BS(html.read(), 'html.parser')

# Find all rows in matches list
tags = bs.find('ul', {'class':'info-list allMatches'}).find_all('li', {'class':''})

# 5th tag always contains a link to the match statistics
matchLinks = [tag.find_all('a')[5].get('href') for tag in tags]

# Extract match statistics
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
                      
if upperLimitFlag:
    matchLinks2 = matchLinks[0:10]
else:
    matchLinks2 = matchLinks

for matchLink in matchLinks2:
    reqMatch = Request(matchLink, headers={'User-Agent':'Mozilla/5.0'} )
    htmlMatch = urlopen(reqMatch)
    bsMatch = BS(htmlMatch.read(), 'html.parser')
    
    matchDate = bsMatch.find('span', {'class':'timezone','data-type':'date_1'}).get_text()
    
    # Ommit first 23 signs ("Premier League Gameweek")
    week = bsMatch.find('div', {'class':'header_matchblock'}).findNext('b').get_text(strip=True)[24:]
    
    teamNames = bsMatch.find_all('strong', {'class':'name'})
    homeTeam = teamNames[0].get_text(strip=True)
    awayTeam = teamNames[1].get_text(strip=True)
    
    # Half time goals
    HTgoals = bsMatch.find('ul', {'class':'add-info'}).findNext('li'). \
        findNext('span').get_text().split('-')
    homeGoalsHT = HTgoals[0]
    awayGoalsHT = HTgoals[1]
    
    # Full time goals
    FTgoals = bsMatch.find('ul', {'class':'add-info'}).findNext('li'). \
        findNext('li').findNext('span').get_text(strip=True).split('-')
    homeGoalsFT = FTgoals[0]
    awayGoalsFT = FTgoals[1]
    
    # Get stats block for further use
    statsBlock = bsMatch.find('div', {'class':'stats-block'})
    
    # Ball possession
    homeBallPos = statsBlock.find('div', {'class':'team-box'}).findNext('strong').get_text()
    awayBallPos = statsBlock.find('div', {'class':'team-box'}). \
        findNext('div', {'class':'team-box'}).findNext('strong').get_text()
    
    # Shots off target
    homeShotsOffTarget = statsBlock.find('div', {'class':'side-one'}). \
        findNext('span', {'class':'num'}).get_text()
    awayShotsOffTarget = statsBlock.find('div', {'class':'side-two'}). \
        findNext('span', {'class':'num'}).get_text()
    
    # Shots on target
    homeShotsOnTarget = statsBlock.find('div', {'class':'inner-box'}). \
        findNext('div', {'class':'side-one'}).findNext('span', {'class':'num'}).get_text()
    awayShotsOnTarget = statsBlock.find('div', {'class':'inner-box'}). \
        findNext('div', {'class':'side-two'}).findNext('span', {'class':'num'}).get_text()
    
    # Corners
    corners = statsBlock.find('strong', {'class':'title'}, string='Corners'). \
        findNext('span', {'class':'num home'})
    homeCorners = corners.get_text()
    awayCorners = corners.findNext('span', {'class':'num'}).get_text()

    # Fouls
    fouls = statsBlock.find('strong', {'class':'title'}, string='Fouls'). \
        findNext('span', {'class':'num home'})
    homeFouls = fouls.get_text()
    awayFouls = fouls.findNext('span', {'class':'num'}).get_text()
    
    # Yellow cards
    yellowCards = statsBlock.find('strong', {'class':'title'}, string='Yellow cards'). \
        findNext('span', {'class':'num home'})
    homeYellowCards = yellowCards.get_text()
    awayYellowCards = yellowCards.findNext('span', {'class':'num'}).get_text()
    
    # Red cards
    redCards = statsBlock.find('strong', {'class':'title'}, string='Red cards'). \
        findNext('span', {'class':'num home'})
    homeRedCards = redCards.get_text()
    awayRedCards = redCards.findNext('span', {'class':'num'}).get_text()
    
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
    
print(stats)
    
# stats.to_json('matchesStats.json')
stats.to_csv('matchesStats.csv')
    
