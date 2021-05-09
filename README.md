# WSSMS2021
The three built scrapers fetch the data from the *footballcritic.com* website.
Particularly from the English Premier League season 2019/2020. It can be found [here](https://www.footballcritic.com/premier-league/season-2019-2020/matches/2/21558).

In order to change the season or the league, you need to change the urls strings in the code.

Script 'run_scraper.sh' measures the execution time of the selected scraper.
To use it uncomment the part of the code with the scraper of your choice and execute
```bash
./run_scraper.sh
```

## BeautifulSoup
To run the scraper just type
```python
python3 getMatchStats.py
```

## Scrapy
Provided files are just the spiders. You need to copy it into the proper project and run it from it's directory.

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
