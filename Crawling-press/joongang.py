from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys

def getText(link):
	req = Request("https://news.joins.com/article/23088120",
	                      headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header_tag = soup.find("h1", {"id": "article_title"})
	date_tag = soup.find("div", {"class": "byline"})
	content_tag =soup.find("div", {"id": "article_body"})

	for tag in content_tag.findAll(True):
			tag.extract()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll(True)[1].text.strip()[3:].replace(".","-")
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()

	return header, date, content
