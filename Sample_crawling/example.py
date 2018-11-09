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

	header_tag = soup.find("span", {"class": "title"})
	date_tag = soup.find("p", {"class": "date-time"})
	content_tag = soup.find("div", {"class": "text"})
	category_tag = soup.find("p", {"class": "category"})
	category = category_tag.find("strong").text.strip()
	author = ""
	if category == "사설.칼럼":
		author = str(content_tag.find("b")).split("<b>")[-1].split("<br/>")[0].strip()
		#author = author_list.split()[0]
	else:
		author_tag = str(header).split('property=\"dable:author\"')
		author_list = author_tag[0].split()[-6:]
	
		
		for i in reversed(author_list):
			if "content=" in i:
				author = i[9:]
				if '"' in author:
					author = author.replace('"',"")
				if ',' in author:
					author = author.split(',')
				break
	
	author.strip()
	
	

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll(True)[0].text.strip()[4:].strip()

	

	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()

	return [header, date, category, author, content]


	
abc = getText("http://www.hani.co.kr/arti/opinion/column/868931.html")
for i in abc:
	print(i)
	print("------------------------------------------------------------")