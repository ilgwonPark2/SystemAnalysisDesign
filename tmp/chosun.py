from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header_tag = soup.find("h1", {"id": "news_title_text_id"})
	date_tag = soup.find("div", {"class": "news_date"})
	content_tag = soup.find("div", {"id": "news_body_id"})
	header=soup.find("head")
	category_tag= str(header).split('property=\"article:section\"') 
	author_tag = str(header).split('property=\"dable:author\"')
	
	content_list = content_tag.findAll("div", {"class": "par"})
	category=category_tag[0].split()[-1][9:-1]
	if "http://life.chosun.com" in link:
		category = "라이프"
		
	author_list = author_tag[0].split()[-5:]
	author=""
	for i in range(len(author_list)):
		if "기자" in author_list[i]:
			if len(author_list[i-1])>6:
				author = author_list[i-1][9:]
				break
			else:
				author = author_list[i-2][9:]
				break
		else:
			author = ""
	if "=" in author:
		author=author.split("=")[-1]

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
	date = date_tag.text.strip()[3:].replace(".","-")
	if ": " in date:
		date = date.replace(": ","")
	if "|" in date:
		date = date.split("|")[0].strip()
	
	

	
	
	return [header, date, category, author, content]



if __name__ == '__main__':
	d2 = date.today()
	d1 = d2 - timedelta(days=30)
	criteria = time.mktime(d1.timetuple())
	page = 1
	while True:
		req = Request(
			"http://search.chosun.com/search/news.search?query=%EB%82%A8%EB%B6%81&pageno={}&orderby=news&naviarraystr=&kind"
			"=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=paging&sdate=&edate=&premium=".format(page))
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		url_collect = []
		###Url Crawling
		second_crawl = soup.find("div", {"class": "search_news_box"}).findAll("dl", {"class": "search_news"})

		for i in second_crawl:
			tag = i.findAll("a")[0]
			print(tag.get("href"))
			article_list = getText(tag.get("href"))
			# 데이트가 범위 밖에 벗어나면 아예 종료 되는 코드
			timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
			if (timestamp < criteria):
				sys.exit()
			for i in article_list:
				print(i)
				print("--------------------------------------------------")
			print("\n\n\n")

		page = page + 1
		print('\n****** Next page *****\n')

		
