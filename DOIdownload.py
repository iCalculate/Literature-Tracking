# coding = UTF-8
# 爬取李东风PDF文档,网址：http://www.math.pku.edu.cn/teachers/lidf/docs/textrick/index.htm
import requests
import time
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def getFile(url):
    file_name = url.split('/')[-1]
    r = requests.get(url, stream=True)

    with open(file_name, 'wb') as f:
        f.write(r.content)
    print ("Sucessful to download" + " " + file_name)


def geturlfromdoi(doi):
    root_url = 'https://sci-hub.tw/'+doi
    strhtml=requests.get(root_url)
    soup = BeautifulSoup(strhtml.text, 'html.parser')
    PDFblock = soup.select('a')
    ret = 'https:' + PDFblock[0].get('onclick')[15:-15]
    return ret

def buildpath():
    if not os.path.exists('pdf_download'):
        os.mkdir('pdf_download')
    os.chdir(os.path.join(os.getcwd(), 'pdf_download'))

buildpath()
doi = '10.1038/s41565-020-0643-3'
url = geturlfromdoi(doi)
print(url)
getFile(url)