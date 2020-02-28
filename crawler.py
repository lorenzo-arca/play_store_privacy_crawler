###############################################################
## Python crawler 1.0 for google play for data extraction    ##
###############################################################

###import statement##
from lxml import etree
from io import StringIO
import requests
from queue import Queue
import play_scraper as pl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import regex as re
import csv

###variable###
CSV_APP_PRIVACY_NAME = "apps_privacy_dataset.csv"
TO_CSV_NUMBER = 10
QUEUE_MAX_SIZE = 10000
START_POINT = "https://play.google.com/store/apps/category/GAME"
visited_links = set()
apps_info_dataset = []
apps_privacy_dataset = []
driver = webdriver.Firefox()


###get_store_infos###
def get_store_infos(id,str):
    global dataset
    global driver
    temp_page = driver.get(str)
    privacy_page = driver.find_element_by_xpath("//a[@jsname='Hly47e']")
    privacy_page.click()
    privacy_elements = driver.find_elements_by_xpath("//li[@class='BCMWSd']")
    regular_expression = re.compile("(<li class=\"BCMWSd\"><span>|</span></li>)")
    privacy_elements_list = [re.sub(regular_expression,"",element.get_attribute("outerHTML")) for element in privacy_elements]
    info = pl.details(id)
    apps_privacy_dataset.append([info.get('app_id'),privacy_elements_list,info.get('price')])





###get_links###
def get_links(tree):
    global visited_links
    return_list = []
    # This will get the anchor tags <a href...>
    refs = tree.xpath("//a")
    # Get the url from the ref
    links = [link.get('href', '') for link in refs]

    for l in links:

        if len(apps_info_dataset)%TO_CSV_NUMBER == 0:

            if len(apps_info_dataset)%10 == 0:
                with open(CSV_APP_PRIVACY_NAME, "w") as f:
                    writer = csv.writer(f)
                    writer.writerows(apps_privacy_dataset)
        str = "https://play.google.com"+l
        if  "/apps/details?id=" in str and str not in visited_links:
                return_list.append(str)
                visited_links.add(str)
                get_store_infos(str.split("?id=")[1],str)
        str = ""
    return return_list


###explore###
def explore(init):
    global dataset
    # Set explicit HTMLParser
    parser = etree.HTMLParser()

    link_queue = Queue(maxsize=QUEUE_MAX_SIZE)

    link_queue.put(init)

    while not link_queue.empty():


        print("QUEUE_SIZE :", link_queue.qsize())

        page_link = link_queue.get()

        print("Exploring: ",page_link)

        page = requests.get(page_link)

        html = page.content.decode("utf-8")

        tree = etree.parse(StringIO(html), parser=parser)

        links = get_links(tree)

        [link_queue.put(l) for l in links]


# Example call
explore(START_POINT)
