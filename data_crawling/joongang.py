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
	header_tag = soup.find("h1", {"id": "article_title"})
	date_tag = soup.find("div", {"class": "byline"})
	content_tag = soup.find("div", {"id": "article_body"})
	header=soup.find("head")
	category_tag=str(header).split('property=\"article:section\"')
	author_tag = str(header).split('property=\"dable:author\"')
	author = author_tag[0].split()[-1][9:-1]
	if "," in author:
		author = author.split(",")[0]
	if len(author)==0:
		author=""
	if(author=='"'):
		author = ""
	category=category_tag[0].split()[-1][9:-1]
	
	for tag in content_tag.findAll(True):
		tag.extract()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll(True)[1].text.strip()[3:].replace(".","-")
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()
	
	return [header, date, category, author, content]


if __name__ == '__main__':
	d2 = date.today()
	d1 = d2 - timedelta(days=1)
	criteria = time.mktime(d1.timetuple())
	page = 1
	while True:
		req = Request('https://search.joins.com/JoongangNews?page={}'
                      '&Keyword=%EB%82%A8%EB%B6%81&SortType=New&SearchCategoryType=JoongangNews'.format(page))
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		url_collect = []

		second_crawl=soup.find("ul",{"class":"list_default"}).findAll("li")
		for i in second_crawl:
			tag = i.findAll("a")[0]
			print(tag.get("href"))
			article_list = getText(tag.get("href"))
			# 데이트 벗어나면 종료 부분
			timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
			if (timestamp < criteria):
				sys.exit()

			# 데이터베이스 연결하는 코드 여기에 작성해야함
			for i in article_list:
				print(i)
				print("-----------------------")
			print("\n\n\n")

		page = page + 1
		print('\n****** Next page *****\n')
