from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
from datetime import datetime
import time
import urllib
import sys

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
					author = author.split(',')[0]
				break
	
	author.strip()
	
	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll(True)[0].text.strip()[4:].strip()

	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()

	return [header, date, category, author, content]

if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=2)
    criteria = time.mktime(d1.timetuple())
    page = 1
    while True:
        req = Request('http://search.hani.co.kr/Search?command=query&keyword=%EB%82%A8%EB%B6%81&media=news&sort=d&period=all&datefrom=2000.01.01&dateto=2018.11.09&pageseq={}'.format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        url_collect = []
		###Url Crawling
        second_crawl=soup.find("ul",{"class":"search-result-list"}).findAll("li")

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
