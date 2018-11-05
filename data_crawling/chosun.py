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
	header_tag = soup.find("h2", {"class": "title"})
	date_tag = soup.find("span", {"class": "date01"})
	content_tag =soup.find("div", {"class": "article_txt"})



	header_tag = header_tag.findAll("h1")[0]


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip()[3:19].replace(".","-")
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()

	return header, date, content



if __name__ == '__main__':
	d2 = date.today()
	d1 = d2 - timedelta(days=1)
	criteria = time.mktime(d1.timetuple())
	f = open('sample_chosun.txt', mode='wt', encoding='utf-8')
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
			print(tag)
			header, date, content = getText(tag.get("href"))
			f.write(header + '\t' + date + '\t' + content + '\n')
			# # 데이트가 범위 밖에 벗어나면 아예 종료 되는 코드 여기에 작성
			timestamp = time.mktime(datetime.strptime(date, '%Y-%m-%d %H:%M').timetuple())
			if (timestamp < criteria):
				sys.exit()

		page = page + 1
		print('\n****** Next page *****\n')
	f.close()
