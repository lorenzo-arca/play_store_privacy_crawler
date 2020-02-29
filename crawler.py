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
from multiprocessing import Process

list = ["https://play.google.com/store/apps/details?id=com.gramgames.mergedragons&hl=en"]

class crawler():

    def __init__(self,csv_name):
        ###variable###
        self.CSV_APP_PRIVACY_NAME = csv_name
        self.TO_CSV_NUMBER = 10
        self.QUEUE_MAX_SIZE = 10000
        self.visited_links = set()
        self.apps_privacy_dataset = []
        self.driver = webdriver.Firefox()
        self.restart_links_number = 0
        self.MAX_LINKS = 150

    ###get_store_infos###
    def get_store_infos(self,id,str):
        temp_page = self.driver.get(str)
        privacy_page = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@jsname='Hly47e']")))
        privacy_page.click()
        privacy_elements = self.driver.find_elements_by_xpath("//li[@class='BCMWSd']")
        regular_expression = re.compile("(<li class=\"BCMWSd\"><span>|</span></li>)")
        privacy_elements_list = [re.sub(regular_expression,"",element.get_attribute("outerHTML")) for element in privacy_elements]
        info = pl.details(id)
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
            if  "/apps/details?id=" in str and str not in self.visited_links:
                if len(self.apps_privacy_dataset)%self.TO_CSV_NUMBER == 0:
                    with open(self.CSV_APP_PRIVACY_NAME, "a") as f:
                        writer = csv.writer(f)
                        writer.writerows(self.apps_privacy_dataset)
                        self.apps_privacy_dataset = []
                return_list.append(str)
                self.visited_links.add(str)
                self.restart_links_number +=1
                self.get_store_infos(str.split("?id=")[1],str)
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
            if (self.restart_links_number>self.MAX_LINKS) ==0:
                    self.driver.quit()
                    self.driver = webdriver.Firefox()
                    self.restart_links_number = 0
            print("QUEUE_SIZE :", link_queue.qsize())
            page_link = link_queue.get()
            print("Exploring: ",page_link)
            page = requests.get(page_link)
            html = page.content.decode("utf-8")
            tree = etree.parse(StringIO(html), parser=parser)
            [link_queue.put(l) for l in self.get_links(tree)]

i = 0
for l in list:
    # Example call

    p = Process(target=crawler(str(i)+".csv").explore, args=(l,))
    p.start()
    i+=1
