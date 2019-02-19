# Code to download mp3 from www.bhagavadgitaclass.com

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import pickle
import os
from sys import exit

cwd = os.getcwd()
html_page = urlopen("http://bhagavadgitaclass.com/")
soup = BeautifulSoup(html_page, "lxml")
links = []
mainDirs = []
allLinks = []
fileNo = 0
for link in soup.findAll('a', attrs={'href': re.compile("^http://bhagavadgitaclass.com/category/bhagavad-gita-chapter-")}):
    links.append(link.get('href'))
    mainDirs.append(link.contents[0])
i=0
for chapterURL in links:
    i+=1
    if not os.path.exists('Chapter '+str(i).zfill(2)):
        os.makedirs('Chapter '+str(i).zfill(2))
    chapLinks = set()
    chapter_html = urlopen(chapterURL).read()
    soup2 = BeautifulSoup(chapter_html, "lxml")
    data = soup2.find("div", {"id": "content"})
    links = data.findAll('a', attrs={'href': re.compile("^http://bhagavadgitaclass.com/bhagavad-gita-")})
    for a in links:
        chapLinks.add(a['href'])
    allLinks.append(sorted(list(chapLinks)));
    print("Chapter",i,"done! Verses found:",len(chapLinks))
c=1
text_file = open("audioNotFound.txt", "w")
for chapter in allLinks:
    print("++++++++++++++++++++++ Chapter",c,"++++++++++++++++++++++")
    i = 1
    for ch in chapter:
        soup3 = BeautifulSoup(urlopen(ch).read(), "lxml")
        
        # elem = soup3.find('a', attrs={'href': re.compile(r"chaitanya-charan")})
        # elem = soup3.find("a", href=re.compile("Chaitanya_Charan", re.I))
        elem = soup3.select_one("a[href*=Chaitanya_Charan]")
        if elem is None:
            elem = soup3.select_one("a[href*=Radhe_Shyam]")
            if elem is None:
                elem = soup3.select_one("a[href*=Prabhupada]")
                if elem is None:
                    elem = soup3.find('a', attrs={'href': re.compile("^http://bhagavadgitaclass.com/wp-content/audio/")})
                    if elem is None:
                        text_file.write("Chapter: "+str(c)+" Index: "+str(i)+'\n')
        if elem is not None:
            r = requests.get(elem.get('href'), allow_redirects=True)
            open('Chapter '+str(c).zfill(2)+'/'+elem.get('href').split('/')[-1], 'wb').write(r.content)
            print("Downloaded Chapter:"+str(c)+" Index:"+str(i))
        i+=1
    c+=1
# print(len(links))
# cwd = os.getcwd()

