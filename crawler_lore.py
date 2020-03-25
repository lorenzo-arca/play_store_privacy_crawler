###############################################################
## Python crawler 1.0 for google play for data extraction    ##
## Flavio Giorgi                                             ##
###############################################################

###import statement##
from lxml import etree
from io import StringIO
import requests
from queue import Queue
import play_scraper as pl
from selenium import webdriver
import regex as re
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading as td
import time
import random
from bs4 import BeautifulSoup
import os
import pickle

# Set number of contemporary threads
n_threads = 4

# Name of txt file for storing list of csv file names
csv_filename = "excel_names"

# Directories
github_dir = "/Users/Lorenzo-Mac/Dropbox/App market - the value of privacy/Scraper/play_store_privacy_crawler/Dataset"
out_dir = github_dir 

###############################################################################
######                import previously founded apps                     ######
###############################################################################

app_id_list = "app_list"

os.chdir(out_dir)

# Open old list
url_1 = "https://play.google.com/store/apps/details?id=" # The first part of the url

try:
    with open(app_id_list + ".txt", "rb") as fp:
        app_list = pickle.load(fp)

    selected_categories = [url_1 + x for x in random.sample(app_list, n_threads )]
    print("Previously downloaded apps founded")

except:
    ###############################################################################
    ######                   Retrive categories names                        ######
    ###############################################################################

    # Base url
    base_url = "https://play.google.com/store/"

    #Url for categories
    search_url = "https://play.google.com/store/apps"
    language = 'hl=en_US'

    page = requests.get(search_url+'?'+language)
    soup = BeautifulSoup(page.text, 'html.parser')

    categories = []

    for x in soup.select("a[href*='/apps/category']"):
        
        # Category name used in the url
        categories.append(x['href'].split('category/',1)[1])

    category_clean = [search_url + '/category/' + x for x in categories if "GAME" not in x and "FAMILY" not in x]
    selected_categories = random.sample(category_clean, n_threads - 2)
    print("No previously downloaded apps founded")


# list = selected categories   
list = ["https://play.google.com/store/apps"
,"https://play.google.com/store/apps/category/GAME",
"https://play.google.com/store/apps/category/FAMILY"]
visited_links = set()
c = td.Condition()
WAIT_CYCLE = 1500


class crawler():

    def __init__(self,csv_name):
        ###variable###
        self.CSV_APP_PRIVACY_NAME = csv_name
        self.TO_CSV_NUMBER = 10
        self.QUEUE_MAX_SIZE = 10000
        global visited_links
        global WAIT_CYCLE
        self.apps_privacy_dataset = []
        self.driver = webdriver.Firefox()
        self.restart_links_number = 0
        self.MAX_LINKS = 100

    ###get_store_infos###
    def get_store_infos(self,id,str):
        info = pl.details(id)
        temp_page = self.driver.get(str)
        privacy_page = WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, "//a[@jsname='Hly47e']")))
        privacy_page.click()
        privacy_elements = []
        privacy_elements = self.driver.find_elements_by_xpath("//li[@class='BCMWSd']")
        i = 0
        while privacy_elements == [] and i < WAIT_CYCLE:
            time.sleep(0.005)
            privacy_elements = self.driver.find_elements_by_xpath("//li[@class='BCMWSd']")
            i+=1
        regular_expression = re.compile("(<li class=\"BCMWSd\"><span>|</span></li>)")
        privacy_elements_list = [re.sub(regular_expression,"",element.get_attribute("outerHTML")) for element in privacy_elements]

        self.apps_privacy_dataset.append([info.get('app_id'),privacy_elements_list,info.get('price'),info.get("iap"),info.get("iap_range")])




    ###get_links###
    def get_links(self,tree):
        return_list = []
        # This will get the anchor tags <a href...>
        refs = tree.xpath("//a")
        # Get the url from the ref
        links = [link.get('href', '') for link in refs]
        for l in links:

            str = "https://play.google.com"+l
            c.acquire()
            if  "/apps/details?id=" in str and str not in visited_links:
                if len(self.apps_privacy_dataset)%self.TO_CSV_NUMBER == 0:
                    with open(self.CSV_APP_PRIVACY_NAME, "a") as f:
                        writer = csv.writer(f)
                        writer.writerows(self.apps_privacy_dataset)
                        self.apps_privacy_dataset = []
                return_list.append(str)
                visited_links.add(str)
                c.notify_all()
                c.release()
                self.restart_links_number +=1
                self.get_store_infos(str.split("?id=")[1],str)
            else:
                c.notify_all()
                c.release()
            str = ""
        return return_list


    ###explore###
    def explore(self,init):
        with open(self.CSV_APP_PRIVACY_NAME, "w") as f:
            writer = csv.writer(f)
        # Set explicit HTMLParser
        parser = etree.HTMLParser()
        link_queue = Queue(maxsize=self.QUEUE_MAX_SIZE)
        link_queue.put(init)

        while not link_queue.empty():
            if (self.restart_links_number>self.MAX_LINKS):
                    self.driver.quit()
                    self.driver = webdriver.Firefox()
                    self.restart_links_number = 0
            print("QUEUE_SIZE :", link_queue.qsize())
            page_link = link_queue.get()
            print("Exploring: ",page_link)
            page = requests.get(page_link)
            if page.status_code != 200: continue
            html = page.content.decode("utf-8")
            tree = etree.parse(StringIO(html), parser=parser)
            [link_queue.put(l) for l in self.get_links(tree)]
        print("Empty QUEUE")
i = 0
name_list = []
for l in list:
    # Example call

    p = td.Thread(target=crawler(str(i)+".csv").explore, args=(l,))
    p.start()
    name_list.append(str(i)+'.csv')
    i+=1

## Save the list obtained          
with open(csv_filename + ".txt", "wb") as fp:
    pickle.dump(name_list, fp)