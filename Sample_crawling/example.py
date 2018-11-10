#-*- coding:utf-8 -*-
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
	header_tag = soup.find("div", {"class": "h_info"}).find("h2")
	date_tag = soup.find("span", {"id": "lblDateLine"})
	category_tag= str(header).split('name=\"article:section\"')
	author_tag = str(header).split('name=\"dable:author\"')
	content_tag = soup.find("div", {"id": "pnlContent"})
	if content_tag is None:
		content_tag = soup.find("div", {"id": "pnlNocutv"})
	

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip()

	category_list = category_tag[0].split()[-6:]
	category = ""
	for i in reversed(category_list):
		if "content=" in i:
			category = i[9:]
			if '"' in category:
				category = category.replace('"',"")
			break
	category.strip()

	author_list = author_tag[0].split()[-6:]
	author = ""
	
	for i in range(len(author_list)):
		if "기자" in author_list[i]:
			author = author_list[i-1]
			if '"' in author:
				author = author.replace('"',"")
			if '·' in author:
				author = author.split('·')[0]
			break
	author.strip()
	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()
	
	return [header, date, category, author, content]



	
abc = getText("http://www.nocutnews.co.kr/news/5058221")
for i in abc:
	print(i)
	print("------------------------------------------------------------")