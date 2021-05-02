# WSSMS2021
The three built scrapers fetch the data from the *Footballcritic.com* website.
Particularly from English Premier League season 2019/2020. It can be found [here](https://www.footballcritic.com/premier-league/season-2019-2020/matches/2/21558).

In order to change the season or the league, you need to change the urls strings in the code.

## BeautifulSoup
To run the scraper just type
```python
python3 proj.py
```

## Scrapy
This scraper runs in two steps:
1. Gather the links to matches websites
    ```python
    scrapy crawl matchLinks -o matchLinks.csv
    ```
    The csv file must be named just like in this example, because it's used in the second step.
1. Gather the data from matches websites
    ```python
    scrapy crawl getStats -o matchStats.csv
    ```

## Selenium
To run the scraper just type
```python
python3 getMatchStats.py
```
