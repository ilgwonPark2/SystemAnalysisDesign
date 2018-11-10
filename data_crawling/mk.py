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

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read().decode('cp949', 'ignore')
	soup = BeautifulSoup(webpage, 'html.parser')
	
	date_tag = soup.find("li", {"class": "lasttime"})
	if date_tag == None:
		date_tag = soup.find("li", {"class": "lasttime1"})
	
	author_tag = soup.find("li", {"class": "author"}).find("a")

	# 날짜 앞의 입력 스트링 제거
	date = date_tag.text.strip()[5:21].replace(".","-")

	up_category_tag = soup.find("li", {"class": "on"})
	if up_category_tag == None:
		category = soup.find("li",{"class":"on_n"}).find("a").text.strip()
	else:
		category_tag = soup.find("dd", {"class": "sub_on"})
		if category_tag != None:
			category = category_tag.text.strip()
		else:
			category = ""

	if category == "오피니언":
		header_tag = soup.find("div",{"class":"view_title"}).find("h3")
		content_tag = soup.find("div", {"class": "view_txt"})
	else:
		header_tag = soup.find("h1", {"class": "top_title"})
		header = header_tag.text.strip()
		content_tag = soup.find("div", {"class": "art_txt"})


	header = header_tag.text.strip()
	if author_tag != None:
		author = author_tag.text.strip()
	else:
		author = ""

	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()
	if "[ⓒ 매일경제 & mk.co.kr, 무단전재 및 재배포 금지]" in content:
		content = content.replace("[ⓒ 매일경제 & mk.co.kr, 무단전재 및 재배포 금지]", "")

	return [header, date, category, author, content]

##selenium사용



if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=1)
    criteria = time.mktime(d1.timetuple())
    #f = open('sample_nocut.txt', mode='wt', encoding='utf-8')
    # 크롬 드라이버 실행
    base_dir = os.getcwd()
    driver = webdriver.Chrome(base_dir + '/chromeforwindow.exe')
    driver.implicitly_wait(10)
    page = 1
    while True:
        # session = requests.Session()
        # session.headers.update({'User-Agent': 'Custom user agent'})
        #
        #
        # headers=session.get('http://www.nocutnews.co.kr/headers')
        # print(headers)

        driver.get('http://find.mk.co.kr/new/search.php?pageNum={}&cat=&cat1=&media_eco'
                   '=&pageSize=20&sub=news&dispFlag=OFF&page=news&s_kwd=%B3%B2%BA%CF&s_page=news&go_page'
                   '=&ord=1&ord1=1&ord2=0&s_keyword=%B3%B2%BA%CF&s_i_keyword=%B3%B2%BA%CF&s_author=&y1'
                   '=1991&m1=01&d1=01&y2=2018&m2=11&d2=06&ord=1&area=ttbd'.format(page))
        result = driver.page_source
        soup = BeautifulSoup(result, 'html.parser')
        second_crawl = soup.find("tr").findAll("span",{"class":"art_tit"})

        for i in second_crawl:
            tag = i.findAll("a")[0]
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

        page = page + 1
        print('\n****** Next page *****\n')






