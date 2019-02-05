# Get all icons under practical-spirituality
# Code to download articles/audios/ppt from www.thespiritualscientist.com Quessionairs

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import pickle

html_page = urlopen("https://www.thespiritualscientist.com/category/practical-spirituality/")
soup = BeautifulSoup(html_page, "lxml")
links = []
fileNo = 0
for link in soup.findAll('a', attrs={'href': re.compile("^https://www.thespiritualscientist.com/20")}):
    links.append(link.get('href'))
links.reverse()
articlesWritten = open("articlesCompleted.txt", "wb+")
#articles = open("articles.txt", "wb+")
#try:
#    b = pickle.load(articles)
#except EOFError:
#    pickle.dump(links,articles)
#else:
#    if len(b)==len(links):
#        print("Articles up to date")
#        links = []
#    else:
#        print("New Articles arrived")
#        fileNo = len(b)
#        links = links[fileNo:]

for link in links:
    fileNo+=1
    if fileNo%50 == 0:
        ask=input("We are continuing. Is there enough time to proceed?\nPress Q or q to quit else any key to continue: ")
        if ask=='q' or ask=='Q':
            pickle.dump(fileNo, articlesWritten)#Do something here
            break;
    print("File #:",fileNo)
    content = urlopen(link).read()
    soup2 = BeautifulSoup(content, "html.parser")
    fileName = link.rsplit('/', 2)[1]
    text_file = open(str(fileNo)+"_"+fileName+".txt", "w")
    for row in soup2.find_all(['h1','span'],attrs={"class" : ["entry-title","author","date"]}):
        text_file.write(row.get_text()+'\n')
    audioSet = set()
    for div in soup2.findAll('a', attrs={'href': re.compile("^http://www.thespiritualscientist.com/audio/")}):
        audioSet.add(div.get('href'))
    if audioSet != set():
        print("Audio found in this file")
    audioNo = 1
    for audio in audioSet:
        name = audio.rsplit('/', 1)[1]
        name = ' '.join(name.split('%20'))
        print("Audio #:",audioNo,name)
        r = requests.get(audio, allow_redirects=True)
        open(str(fileNo)+'_'+name, 'wb').write(r.content)
        audioNo+=1
    for ans in soup2.findAll('p'):
        if 'Please type the characters of this captcha image in the input box' in ans.get_text():
            break;
        text_file.write(ans.get_text()+'\n')
    text_file.close()
    #break;

