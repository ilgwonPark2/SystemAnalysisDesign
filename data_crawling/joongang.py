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



if __name__ == '__main__':

	d2 = date.today()
	d1 = d2 - timedelta(days=1)
	criteria = time.mktime(d1.timetuple())
	f = open('sample_joonang.txt', mode='wt', encoding='utf-8')
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
			header, date, content = getText(tag.get("href"))
			f.write(header + '\t' + date + '\t' + content + '\n')
			# # 데이트가 범위 밖에 벗어나면 아예 종료 되는 코드 여기에 작성
			timestamp = time.mktime(datetime.strptime(date, '%Y-%m-%d %H:%M').timetuple())
			if (timestamp < criteria):
				sys.exit()
		page = page + 1
		print('\n****** Next page *****\n')
	f.close()
