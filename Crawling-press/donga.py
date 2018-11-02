from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
from datetime import datetime
import time
import urllib
import sys


def donga(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header_tag = soup.find("h2", {"class": "title"})
	date_tag = soup.find("span", {"class": "date01"})
	content_tag =soup.find("div", {"class": "article_txt"})



	for tag in content_tag.findAll(True):
		tag.extract()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text[3:]
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()

	return header, date, content





	


if __name__ == '__main__':
	d2 = date.today()
	d1 = d2 - timedelta(days=1)
	criteria = time.mktime(d1.timetuple())
	page = 1
	while True:
		req = Request("http://news.donga.com/search?p={}&query=%EB%82%A8%EB%B6%81&check_news=16&more=1&sorting=1&search_date=1&v1=&v2=&range=1".format(page))
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		url_collect = []
        ###Url Crawling
		second_crawl = soup.find("div", {"class": "searchCont"}).findAll("p", {"class": "tit"})

		for i in second_crawl:
			tag = i.findAll("a")[0]
			for a in tag.findAll(True):
				a.extract()
			header, date, content = donga(tag.get("href"))
			# 데이트가 범위 밖에 벗어나면 아예 종료 되는 코드 여기에 작성
			timestamp = time.mktime(datetime.strptime(date, '%Y-%m-%d %H:%M').timetuple())
			if(timestamp < criteria):
				sys.exit()
			print(header) 
			print(date) 
			print(content+"\n")


		page=page+15
		print('\n****** Next page *****\n')