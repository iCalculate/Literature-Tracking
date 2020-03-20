import requests        #导入requests包
import re
from bs4 import BeautifulSoup

JournalList = ['nmat', 'natcatal', 'natelectron', 'nphys', 'natrevchem', 'nnano', 'nenergy', 'nchem']
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

    output = open('RecentPaper\\'+JournalList[loop]+'-data.txt', 'w', encoding='utf-8')
    for row in Ans:
        rowtxt = '{},{},{},{},{},{}'.format(row[0],row[1],row[2],row[3],row[4],row[5])
        output.write(rowtxt)
        output.write('\n')
    output.close()

