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

	header_tag = soup.find("h1", {"id": "news_title_text_id"})
	date_tag = soup.find("div", {"class": "news_date"})
	content_tag = soup.find("div", {"id": "news_body_id"})
	header=soup.find("head")
	category_tag=str(header).split('property=\"article:section\"')
	
	content_list = content_tag.findAll("div", {"class": "par"})
	category=category_tag[0].split()[-1][9:-1]

	content = ""
	if(category=="연예"):
		for i in content_list[:-1]:
			content += " " + i.text.strip()
			content.strip()
	else:
		for i in content_list:
			content += " " + i.text.strip()
			content.strip()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip()[3:19].replace(".","-")

	
	
	return [header, date, category, content]


abc = getText("http://news.chosun.com/site/data/html_dir/2018/11/07/2018110702174.html")
for i in abc:
	print(i)
	print("------------------------------------------------------------")