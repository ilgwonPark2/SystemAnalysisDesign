from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
from datetime import datetime
import time
import urllib
import sys
import csv

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')


	category_tag = soup.find("div", {"class": "sec_title"})
	category = category_tag.text.strip()
	if category == "마켓·비즈" or category == "라이프":
		header_tag = soup.find("h1", {"id": "articleTtitle"})
	else:
		header_tag = soup.find("h1", {"id": "article_title"})
	date_tag = soup.find("div", {"class": "byline"})


	author_tag = soup.find("span", {"class":"name"})
	content_tag =soup.findAll("p", {"class": "content_text"})

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.find("em").text[5:-3].strip().replace(".","-")

	if author_tag.text=="":
		author = ""
	else:
		author = author_tag.text.split()[0]
	if "·" in author:
		author = author.split("·")[0]
	author.strip()

	content=""
	for i in content_tag:
		content += i.text + " "
	content.strip()

	return [header, date, category, author, content]





if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=3)
    criteria = time.mktime(d1.timetuple())
    page = 0
    # csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'khan_3day.csv'
    f = open("sample_data/"+filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["제목","날짜","분류", "기자", "본문"])
    while True:
        req = Request('http://search.khan.co.kr/search.html?stb=khan&q=%EB%82%A8%EB%B6%81&pg={}&sort=1'.format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        url_collect = []
		###Url Crawling
        second_crawl=soup.find("div",{"class":"news section"}).findAll("dl",{"class":"phArtc"})

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print(tag.get("href"))
            article_list = getText(tag.get("href"))
			# 데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
            timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
            if(timestamp < criteria):
                f.close()
                sys.exit()
			# 요기에다가 mysql로 보내는 코드 작성해야합니다
            for i in article_list:
                print(i)
                print("---------------------------------------")
            wr.writerow(article_list)
            print("\n\n\n")

        page = page + 1
        print('\n****** Next page *****\n')
