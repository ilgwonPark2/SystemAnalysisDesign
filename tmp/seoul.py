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
	header_tag = soup.find("h1", {"class": "atit2"})
	date_tag = soup.find("p", {"class": "v_days"})
	category_tag= str(header).split('property=\"article:section\"')
	author_tag = str(header).split('property=\"dable:author\"')
	content_tag = soup.find("div", {"class": "v_article"})
	

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.find('span').text.strip()

	category_list = category_tag[0].split()[-6:]
	category = ""
	for i in reversed(category_list):
		if "content=" in i:
			category = i[9:]
			if '"' in category:
				category = category.replace('"',"")
			break
	category.strip()

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
    while True:
        req = Request('http://search.seoul.co.kr/index.php?keyword=%EB%82%A8%EB%B6%81&pageNum={}'.format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
		###Url Crawling
        second_crawl=soup.find("div",{"id":"list_area"}).findAll("dl",{"class":"article"})

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print(tag.get("href"))
            if "http://go.seoul.co.kr" not in tag.get("href"):
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

        page = page + 1
        print('\n****** Next page *****\n')