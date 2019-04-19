#!/usr/bin/env python
# coding: utf-8

#Unique Weblink Scrapper 

#import all required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.request import urlopen

#get the html code and text
url = "https://www.census.gov/programs-surveys/popest.html"
page = requests.get(url)    
data = page.text
soup = BeautifulSoup(data, features="lxml")

links=[]
for link in soup.find_all('a'):
    links.append(link.get('href'))
    

#cleaning up the links 
first_char=[str(l)[:1] for l in links]
first_char=pd.Series(first_char)
dead_link=first_char.str.contains('N', regex=True)
unrecognized=first_char.str.contains('/', regex=True)
hashtags=first_char.str.contains('#', regex=True)
list(dict.fromkeys(links))
dict_link={'links':links, 'dead_link':dead_link, 'unrecognized':unrecognized, 'hashtags':hashtags}
df=pd.DataFrame(dict_link)
df=df[df['dead_link']==False]
df=df[df['unrecognized']==False]
df=df[df['hashtags']==False]
df=df.iloc[1:]
df=df[df['links']!='https://www.linkedin.com/company/us-census-bureau/']
df=df.iloc[:-1]

#retrieve actual links
absolute_links=[]
for url in df['links']:
    result = urlopen(url)
    absolute_links.append(result.geturl())

#remove duplicate links 
absolute_links=pd.Series(absolute_links)
unique_links=absolute_links.drop_duplicates(keep='first')
print(len(absolute_links))
print(len(unique_links))

#Print out html code
print(soup)

#create pandas dataframe and save as csv file
dict_link={'unique_links':unique_links}
df1=pd.DataFrame(dict_link)
df1.to_csv('unique_weblinks.csv')
df1.tail(10)
