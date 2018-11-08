from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys
import csv

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header=soup.find("head")
	header_tag = soup.find("header", {"class": "article-header"}).find("h3")
	date_tag = soup.find("div", {"class": "info"})
	content_tag =soup.find("div", {"id": "article_story"})
	category_tag = str(header).split('property=\"article:section\"')
	author_tag = str(header).split('property=\"dable:author\"')
	
	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.findAll("p")[0].text[3:].strip().replace(".","-")

	category = category_tag[0].split()[-1][9:-1]

	author = author_tag[0].split()[-1][9:-1]

	# 컨텐트에 앞뒤 공백 제거
	content_list = content_tag.findAll("p")
	content=""
	for i in content_list:
		content += i.text + " "
	content.strip()

	return [header, date, category, author, content]





if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=7)
    criteria = time.mktime(d1.timetuple())
    page = 1
	# csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'hkilbo_1week.csv'
    f = open("sample_data/"+filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["제목","날짜","분류","기자","본문"])
    while True:
        req = Request('http://search.hankookilbo.com/v2/?stype=&ssort=1&page={}&'
                      'cddtc=&cate_str=&sword=%EB%82%A8%EB%B6%81&sfield=&sdate=&edate='.format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
		###Url Crawling
        second_crawl=soup.find("ul",{"class":"article-list"}).findAll("li",{"class":"item"})

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print(tag.get("href"))
            article_list = getText(tag.get("href"))
			# 데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
            timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
            if(timestamp < criteria):
                f.close()
                sys.exit()
            wr.writerow(article_list)
			# 요기에다가 mysql로 보내는 코드 작성해야합니다
            for i in article_list:
                print(i)
                print("---------------------------------------")
            print("\n\n\n")
        page = page + 1
        print('\n****** Next page *****\n')