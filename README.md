# Play_store Crawler


This crawler is designed to explore google playstore and retrive useful information
about apps. Moreover, **it can retrive also privacy permission used from each apps**.

## Required packages
```
pip install selenium
pip install xlml
pip install play_scraper
```
## KNOWLEDGE

Dataset headline: [APP_ID,PERMISSION,PRICE,IN-APP_PURCHASE, IN-APP_PURCHASE_PRICE_RANGE]

The code below allows to set:
- name
- save threshold
- queue max size
- maximum number of explored links before ram cleaning

```python3
self.CSV_APP_PRIVACY_NAME = csv_name
self.TO_CSV_NUMBER = 10
self.QUEUE_MAX_SIZE = 10000
self.MAX_LINKS = 150
```
## How does it work?

The crawler is based on BFS search. It starts the search from a single strarting point (if it's executed as a single process) or from a multiple starting points. In order to occupy a reasonable amount of RAM the crawler allows to visit only a predefined amount of links before it clean up the current session and starts another.
The program appends information obtained into a csv file and then clean them up.

## LORE MODS

crawler_categories.py crawl google play starting from categories (4 selected at random) and save csv files with the results and a txt file with file names for create_app_list

create_app_list.py import the csv files, extract the app link and store it in a txt. If the txt already exists, it adds to the existing list the new app links

crawler_existing_applist.py works as crawler_categories.py but the starting points are some apps choosen at random from the list created by create_app_list.py


