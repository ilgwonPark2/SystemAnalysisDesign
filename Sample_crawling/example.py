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
	header_tag = soup.find("h1", {"id": "article_title"})
	date_tag = soup.find("div", {"class": "byline"})
	content_tag = soup.find("div", {"id": "article_body"})
	header=soup.find("head")
	category_tag=str(header).split('property=\"article:section\"')
	
	category=category_tag[0].split()[-1][9:11]

	for tag in content_tag.findAll(True):
		tag.extract()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll(True)[1].text.strip()[3:].replace(".","-")
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()
	
	return [header, date, category, content]


abc = getText("https://news.joins.com/article/23102876")
for i in abc:
	print(i)
	print("------------------------------------------------------------")