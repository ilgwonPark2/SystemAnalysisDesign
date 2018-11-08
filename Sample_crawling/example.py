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
	header_tag = soup.find("h2", {"class": "title"})
	date_tag = soup.find("span", {"class": "date01"})
	content_tag =soup.find("div", {"class": "article_txt"})
	category_tag = soup.find("div", {"class": "location"})
	another_content = content_tag.findAll("div")
	author_tag = str(header).split('property=\"dable:author\"')
	author_list = author_tag[0].split()[-6:-1]
	author=""
	for i in range(len(author_list)):
		if 'content="' in author_list[i]:
			author = author_list[i][9:]
			break
		else:
			author = ""
	for tag in content_tag.findAll(True):
		tag.extract()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text[3:]
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()

	for i in another_content:
		content += " " + i.text.strip()
	content.strip()
	category = category_tag.text.strip()

	return [header, date, category, author, content]

	
abc = getText("http://news.donga.com/3/all/20181107/92760724/1")
for i in abc:
	print(i)
	print("------------------------------------------------------------")