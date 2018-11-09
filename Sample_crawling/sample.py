#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
import urllib
from selenium import webdriver
import os

def getText(link):
	category=""
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read().decode('cp949', 'ignore')
	soup = BeautifulSoup(webpage, 'html.parser')
	
	date_tag = soup.find("li", {"class": "lasttime"})
	if date_tag == None:
		date_tag = soup.find("li", {"class": "lasttime1"})
	author_tag = soup.find("li", {"class": "author"})
	#author_tag = soup.find("li", {"class": "author"}).find("a")

	# 날짜 앞의 입력 스트링 제거
	#date = date_tag.text.strip()[5:21].replace(".","-")

	up_category_tag = soup.find("li", {"class": "on"})
	if up_category_tag == None:
		category_tag = soup.find("li",{"class":"on_n"})#.find("a").text.strip()
	else:
		category_tag = soup.find("dd", {"class": "sub_on"})
		if category_tag != None:
			category = category_tag.text.strip()
		else:
			category = ""

	if category == "오피니언":
		header_tag = soup.find("div",{"class":"view_title"}).find("h3")
		content_tag = soup.find("div", {"class": "view_txt"})
	else:
		header_tag = soup.find("h1", {"class": "top_title"})
		#header = header_tag.text.strip()
		content_tag = soup.find("div", {"class": "art_txt"})


	#header = header_tag.text.strip()

    
	if author_tag != None:
		author = author_tag.text.strip()
	else:
		author = ""

	#for i in content_tag.findAll(True):
	#	i.extract()
	#content = content_tag.text.strip()
	#if "[ⓒ 매일경제 & mk.co.kr, 무단전재 및 재배포 금지]" in content:
	#	content = content.replace("[ⓒ 매일경제 & mk.co.kr, 무단전재 및 재배포 금지]", "")

	return [header_tag, date_tag, category_tag, author_tag, content_tag]


	
abc = getText("http://opinion.mk.co.kr/view.php?year=2018&no=702156")
for i in abc:
	print(i)
	print("------------------------------------------------------------")