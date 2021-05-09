#!/bin/bash

SECONDS=0

# Uncomment selected part to measure its execution time.
# Provide proper paths to the scrapers' files

## BS part
# python3 ./getMatchStats.py

## Selenium part
# python3 ./selenium/getMatchStats.py

## Scrapy part
# scrapy crawl matchLinks -o matchLinks.csv
# scrapy crawl getStats -o matchStats.csv

DURATION=$SECONDS

echo "Duration of the process: $DURATION"
