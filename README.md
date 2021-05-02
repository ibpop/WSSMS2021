# WSSMS2021

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
scrapy crawl getStats -o getStats.csv
```

## Selenium
To run the scraper just type
```python
python3 getMatchStats.py
```
