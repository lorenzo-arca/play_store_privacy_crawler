###############################################################
## Python crawler 1.0 for google play                        ##
###############################################################


###import statement##
from lxml import etree
from io import StringIO
import requests
from queue import Queue
import pandas as pd
import play_scraper as pl

###variable###
visited_links = set()
dataset = []


###analisys###
def analisys(tree):
    return None


def get_store_infos(id):
    global dataset
    dataset.append(pl.details(id))
    print("YES")



###get_links###
def get_links(tree):
    return_list = []
    global visited_links
    # This will get the anchor tags <a href...>
    refs = tree.xpath("//a")
    # Get the url from the ref
    links = [link.get('href', '') for link in refs]
    for l in links:
        str = "https://play.google.com"+l
        if  "/apps/details?id=" in str and str not in visited_links:
                return_list.append(str)
                visited_links.add(str)
                get_store_infos(str.split("?id=")[1])
        str = ""
    return return_list




###explore method###

def explore(init):
    global dataset
    # Set explicit HTMLParser
    parser = etree.HTMLParser()

    link_queue = Queue(maxsize=10000)

    link_queue.put(init)

    while not link_queue.empty():
        print(link_queue.qsize())
        page_link = link_queue.get()

        print("Exploring: ",page_link)
        page = requests.get(page_link)

        if len(dataset) > 100:
            df = pd.DataFrame(dataset)
            df.to_csv("/home/flavio/Scrivania/info.csv")

        # Decode the page content from bytes to string
        html = page.content.decode("utf-8")

        # Create your etree with a StringIO object which functions similarly
        # to a fileHandler
        tree = etree.parse(StringIO(html), parser=parser)

        links = get_links(tree)
        # Call this function and pass in your tree
        [link_queue.put(l) for l in links]


# Example call
explore("https://play.google.com/store/apps/category/GAME")
