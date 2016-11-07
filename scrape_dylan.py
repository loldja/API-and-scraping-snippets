import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import os
from time import sleep

artist_dict = {}

url = 'http://www.songlyrics.com/bob-dylan-lyrics/'
response = requests.get(url)
page = response.text
page = BeautifulSoup(page, 'lxml')
for j in page.find_all(href=re.compile("http://www.songlyrics.com/bob-dylan/.*lyrics")):
    artist_dict[j.text] = j['href']

songs_list = []
lyrics_dict = {}

count = 1

for k,v in artist_dict.items():
    url = "%s"%(v)
    response = requests.get(url)
    page = response.text
    page = BeautifulSoup(page, 'lxml')
    lyrics = page.find('p', id='songLyricsDiv')
    lyrics_dict[k] = {v, lyrics}
    sleep(0.03)
    
    df = pd.DataFrame(lyrics_dict)
    df.to_csv(r'~/Notebooks/lyrics_data2/%s.csv' % count)
    count += 1