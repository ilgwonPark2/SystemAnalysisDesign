from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
import urllib
from selenium import webdriver
import os

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header=soup.find("head")
	header_tag = soup.find("header", {"class": "article-header"}).find("h3")
	date_tag = soup.find("div", {"class": "info"})
	content_tag =soup.find("div", {"id": "article_story"})
	category_tag = str(header).split('property=\"article:section\"')
	author_tag = str(header).split('property=\"dable:author\"')
	
	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll("p")[0].text[3:].strip().replace(".","-")

	category = category_tag[0].split()[-1][9:-1]

	author = author_tag[0].split()[-1][9:-1]

	# 컨텐트에 앞뒤 공백 제거
	content_list = content_tag.findAll("p")
	content=""
	for i in content_list:
		content += i.text + " "
	content.strip()

	return [header, date, category, author, content]

	
abc = getText("http://www.hankookilbo.com/News/Read/201811081659791046")
for i in abc:
	print(i)
	print("------------------------------------------------------------")