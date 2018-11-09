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
	header=soup.find("head")
	header_tag = soup.find("h1", {"class": "title"})
	date_tag = soup.find("span", {"class": "time"})
	category_tag = soup.find("a", {"class": "sub_tag"})
	#category_tag= str(header).split('property=\"article:section\"')
	author_tag = str(header).split('property=\"dable:author\"')
	content_tag = soup.find("div", {"id": "newsView"})
	

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip().replace(".","-")

	category = category_tag.text.strip()

	author_list = author_tag[0].split()[-6:]
	author = ""
	for i in reversed(author_list):
		if "content=" in i:
			author = i[9:]
			if '"' in author:
				author = author.replace('"',"")
			if '/' in author:
				author = author.split('/')[0]
			break
	author.strip()
	
	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()

	return [header, date, category, author, content]





if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=3)
    criteria = time.mktime(d1.timetuple())
    page = 1
    # csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'hankyung_3day.csv'
    f = open("sample_data/"+filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["제목","날짜","분류", "기자", "본문"])
    while True:
        req = Request('http://search.hankyung.com/apps.frm/search.news?query='
                      '%EB%82%A8%EB%B6%81&mediaid_clust=HKPAPER,HKCOM&page={}'.format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
		###Url Crawling
        second_crawl=soup.find("ul",{"class":"article"}).findAll("li")

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print(tag.get("href"))
            if "http://plus.hankyung.com" not in tag.get("href"):
                article_list = getText(tag.get("href"))
			    # 데이트가 범위 밖에 벗어나면 아예 종료 되는 코드
                timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
                if (timestamp < criteria):
                    f.close()
                    sys.exit()
                for i in article_list:
                    print(i)
                    print("--------------------------------------------------")
                wr.writerow(article_list)
                print("\n\n\n")

        page = page + 1
        print('\n****** Next page *****\n')