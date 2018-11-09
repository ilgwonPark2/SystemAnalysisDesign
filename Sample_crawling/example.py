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
	header_tag = soup.find("h1", {"class": "title"})
	date_tag = soup.find("span", {"class": "time"})
	category_tag = soup.find("a", {"class": "sub_tag"})
	#category_tag= str(header).split('property=\"article:section\"')
	author_tag = str(header).split('property=\"dable:author\"')
	content_tag = soup.find("div", {"id": "newsView"})
	

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip().replace(".","-")

	"""
	category_list = category_tag[0].split()[-6:]
	category = ""
	for i in reversed(category_list):
		if "content=" in i:
			category = i[9:]
			if '"' in category:
				category = category.replace('"',"")
			break
	category.strip()
	"""
	category = category_tag.text.strip()

	author_list = author_tag[0].split()[-6:]
	author = ""
	for i in reversed(author_list):
		if "content=" in i:
			author = i[9:]
			if '"' in author:
				author = author.replace('"',"")
			if '/' in author:
				author = author.split('/')[0]
			break
	author.strip()
	
	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()

	return [header, date, category, author, content]


	
abc = getText("http://plus.hankyung.com/apps/newsinside.view?aid=201811050745A")
for i in abc:
	print(i)
	print("------------------------------------------------------------")