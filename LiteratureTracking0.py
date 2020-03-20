import requests        #导入requests包
import re
from bs4 import BeautifulSoup

def gettext():
    txt = open("RecentPaper/NameList.txt", "r", errors='ignore').read()
    txt = txt.lower()
    for ch in '!"#$&()*+,-./:;<=>?@[\\]^_{|}·~‘’':
        txt = txt.replace(ch, "")
    return txt

JournalList = ['nmat', 'natcatal', 'natelectron', 'nphys', 'natrevchem', 'nnano', 'nenergy', 'nchem']
RelaAns = [['Number', 'Time', 'Format', 'Title', 'DOI', 'link']]
RelaCount = 0
NameList = [['Title']]

for loop in range(len(JournalList)):
    url='https://www.nature.com/'+JournalList[loop]+'/research'
    strhtml=requests.get(url)
    soup=BeautifulSoup(strhtml.text, 'html.parser')
    TitleData = soup.select('#content > div.container.cleared.container-type-article-list > div > div > div > div > div > ul > li > article > div > h3 > a')
    TimeData = soup.select('#content > div.container.cleared.container-type-article-list > div > div > div > div > div > ul > li > article > div > p > time')
    FormatData = soup.select('#content > div.container.cleared.container-type-article-list > div > div > div > div > div > ul > li > article > div > p > span')

    Ans = [['Number', 'Time', 'Format', 'Title', 'DOI', 'link']]
    Aped = Ans[0]
    for count in range(len(TimeData)):
        Ans.append([count+1, TimeData[count].get_text(), FormatData[int((count) * 2)].get_text(), \
            TitleData[count].get_text()[42:], '10.1038' + TitleData[count].get('href')[9:], \
           'https://www.nature.com' + TitleData[count].get('href')])

        NameList.append([TitleData[count].get_text()[42:]])

        if (re.search(r'reduction', TitleData[count].get_text()[42:])):
            RelaAns.append([RelaCount, TimeData[count].get_text(), FormatData[int((count) * 2)].get_text(), \
                        TitleData[count].get_text()[42:], '10.1038' + TitleData[count].get('href')[9:], \
                        'https://www.nature.com' + TitleData[count].get('href')])
            RelaCount += 1

    output = open('RecentPaper\\'+JournalList[loop]+'-data.txt', 'w', encoding='utf-8')
    for row in Ans:
        rowtxt = '{},{},{},{},{},{}'.format(row[0],row[1],row[2],row[3],row[4],row[5])
        output.write(rowtxt)
        output.write('\n')
    output.close()

output = open('RecentPaper/Rela-data.txt', 'w', encoding='utf-8')
for row in RelaAns:
    rowtxt = '{},{},{},{},{},{}'.format(row[0],row[1],row[2],row[3],row[4],row[5])
    output.write(rowtxt)
    output.write('\n')
output.close()

output = open('RecentPaper/NameList.txt', 'w', encoding='utf-8')
for row in NameList:
    rowtxt = '{}'.format(row[0])
    output.write(rowtxt)
    output.write('\n')
output.close()

txt = gettext()
words = txt.split()
counts = {}
for word in words:
    counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
for i in range(100):
    word,count = items[i]
    print("{0:<10}{1:>5}".format(word,count))
