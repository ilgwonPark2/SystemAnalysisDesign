import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
from datetime import datetime
import time
import urllib
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

##selenium사용
def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')
	header=soup.find("head")
	header_tag = soup.find("div", {"class": "h_info"}).find("h2")
	date_tag = soup.find("span", {"id": "lblDateLine"})
	category_tag= str(header).split('name=\"article:section\"')
	author_tag = str(header).split('name=\"dable:author\"')
	content_tag = soup.find("div", {"id": "pnlContent"})
	if content_tag is None:
		content_tag = soup.find("div", {"id": "pnlNocutv"})
	

	header = header_tag.text.strip()
	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip()

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
	
	for i in range(len(author_list)):
		if "기자" in author_list[i]:
			author = author_list[i-1]
			if '"' in author:
				author = author.replace('"',"")
			if '·' in author:
				author = author.split('·')[0]
			break
	author.strip()
	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()
	
	return [header, date, category, author, content]


if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=2)
    criteria = time.mktime(d1.timetuple())
    #f = open('sample_nocut.txt', mode='wt', encoding='utf-8')
    # 크롬 드라이버 실행
    base_dir = os.getcwd()
    driver = webdriver.Chrome(base_dir + '/chromeforwindow.exe')
    driver.implicitly_wait(10)
    page = 0
    # csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'nocut_2day.csv'
    f = open("sample_data/"+filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["제목","날짜","분류", "기자", "본문"])
    while True:
        # session = requests.Session()
        # session.headers.update({'User-Agent': 'Custom user agent'})
        #
        #
        # headers=session.get('http://www.nocutnews.co.kr/headers')
        # print(headers)

        driver.get('http://search.nocutnews.co.kr/list?sk=2&sv=%EB%82%A8%EB%B6%81&sp=0&ot=2&sc=0&pageIndex={}&a=Center'.format(page))
        result = driver.page_source
        soup = BeautifulSoup(result, 'html.parser')

        second_crawl = soup.find("ul", {"class": "newslist"}).findAll("li")
        

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







