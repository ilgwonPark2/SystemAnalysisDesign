from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys
import MySQLdb


def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header=soup.find("head")
	header_tag = soup.find("h2", {"class": "title"})
	date_tag = soup.find("span", {"class": "date01"})
	content_tag =soup.find("div", {"class": "article_txt"})
	category_tag = soup.find("div", {"class": "location"})
	another_content = content_tag.findAll("div")
	author_tag = str(header).split('property=\"dable:author\"')
	author_list = author_tag[0].split()[-6:-1]
	author=""
	for i in range(len(author_list)):
		if 'content="' in author_list[i]:
			author = author_list[i][9:]
			break
		else:
			author = ""
	for tag in content_tag.findAll(True):
		tag.extract()


	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text[3:]
	# 컨텐트에 앞뒤 공백 제거
	content = content_tag.text.strip()

	for i in another_content:
		content += " " + i.text.strip()
	content.strip()
	category = category_tag.text.strip()

	return [header, date, category, author, content]

if __name__ == '__main__':
	# db=MySQLdb.connect(host="localhost", user="root",passwd="cloudera",db="mysql")
	# db.set_character_set('utf8')

	# cursor=db.cursor()
    #
	# sql="INSERT "
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
			print(tag.get("href"))
			article_list = getText(tag.get("href"))
			# 데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
			timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
			if(timestamp < criteria):
				sys.exit()
			# 요기에다가 mysql로 보내는 코드 작성해야합니다
			for i in article_list:
				print(i)
				print("---------------------------------------")
			print("\n\n\n")
			


		page=page+15
		print('\n****** Next page *****\n')