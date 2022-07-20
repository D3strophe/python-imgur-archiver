import requests
import os 
import time
import sys 
from bs4 import BeautifulSoup
import pandas as pd

TIMESTAMP = time.strftime("%b-%d-%y %I%M", time.gmtime())

query = sys.argv[1]
print(sys.argv)

def gallery_url_query(search):
    URLS = [""]
    string = (f"https://imgur.com/search?q={search}")
    print(string)
    request = requests.get(string)
    print(request)
    soup = BeautifulSoup(request.text, "html.parser")
    
    images = soup.find_all("a")
    for image in images: URLS.append(image.get("href"))

    return URLS

def gallery_url_dataframe(array):
    dataframe = pd.DataFrame({"URLS": array})
    print(dataframe)
    dataframe["UNIQUE_HASH"] = abs(dataframe[["URLS"]].sum(axis=1).map(hash))
    dataframe["URLS"] = dataframe["URLS"].str.extract(r'(/gallery/[a-zA-Z0-9]*)')
    dataframe = dataframe.dropna(axis='rows')
    dataframe["URLS"] = "https://imgur.com" + dataframe["URLS"].astype(str) 
    dataframe["ARCHIVE_DATE"] = TIMESTAMP 
    
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe

link_frame = gallery_url_dataframe(gallery_url_query(query))
print(f"Gathered {len(link_frame)} link(s)")

try: os.mkdir("Archives")
except: print("The Archives are intact")

link_frame.to_csv(f"Archives/Imgur Query {TIMESTAMP}.csv", sep='\t')
print(f"New query is written to path: Archives/Imgur Query {TIMESTAMP}.csv")