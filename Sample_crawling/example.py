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


	category_tag = soup.find("div", {"class": "sec_title"})
	category = category_tag.text.strip()
	if category == "마켓·비즈" or category == "라이프":
		header_tag = soup.find("h1", {"id": "articleTtitle"})
	else:
		header_tag = soup.find("h1", {"id": "article_title"})
	date_tag = soup.find("div", {"class": "byline"})


	author_tag = soup.find("span", {"class":"name"})
	content_tag =soup.findAll("p", {"class": "content_text"})

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.find("em").text[5:-3].strip().replace(".","-")

	#category = category_tag.text.strip()
	if author_tag.text=="":
		author = ""
	else:
		author = author_tag.text.split()[0]
	if "·" in author:
		author = author.split("·")[0]
	author.strip()

	#author_list = author_tag[0].split()[-6:]
	#author=""
	#for i in range(len(author_list)):
	#	if 'content="' in author_list[i]:
	#		author = author_list[i][9:-1]
	#		break
	#	else:
	#		author = ""

	# 컨텐트에 앞뒤 공백 제거
	content=""
	for i in content_tag:
		content += i.text + " "
	content.strip()

	return [header, date, category, author, content]


	
abc = getText("http://biz.khan.co.kr/khan_art_view.html?artid=201811062129005&code=920101")
for i in abc:
	print(i)
	print("------------------------------------------------------------")