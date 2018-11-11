from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
#from sshtunnel import SSHTunnelForwarder
import urllib
import sys
#import MySQLdb
from selenium import webdriver
import os
import csv
#

def getText(link, driver):
	driver.get(link)
	result = driver.page_source
	soup = BeautifulSoup(result, 'html.parser')

	header= soup.find("h2", {"id": "titleapp"}).find("div").text.strip()
	
	date_list = soup.find("div", {"class": "headline-data"}).text.strip().split("KST")[0][12:].split()
	hour = date_list[-1]

	rest = date_list[0].split(".")
	month = rest[0]
	day = rest[1].split(",")[0]
	year = rest[1].split(",")[-1]

	if "Jan" == month:
		month = "01"
	elif "Feb" == month:
		month = "02"
	elif "Mar" == month:
		month = "03"
	elif "Apr" == month:
		month = "04"
	elif "May" == month:
		month = "05"
	elif "Jun" == month:
		month = "06"
	elif "Jul" == month:
		month = "07"
	elif "Aug" == month:
		month = "08"
	elif "Sep" == month:
		month = "09"
	elif "Oct" == month:
		month = "10"
	elif "Nov" == month:
		month = "11"
	elif "Dec" == month:
		month = "12"
	if len(day)==1:
		day = "0"+day
	date = year + "-" + month +"-"+day+" " + hour
	category = soup.find("div", {"class": "view_map"}).find("span").findAll("a")[-1].text.strip()


	content_tag = soup.find("div", {"id": "bodyapp"}).find("div")
	
	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()

	author = ""
	try:
		author_list = content.split('Please direct comments or questions to')[0].strip().split()[-16:]
		for i in range(len(author_list)):
			if "By" in author_list[i]:
				author += author_list[i+1] + " " +  author_list[i+2]
				break	
		if "," in author:
			author = author.replace(",","")
	except:
		author= ""
	
	
	return [header, date, category, author, content]



if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=30)
    criteria = time.mktime(d1.timetuple())
    # f = open('sample_nocut.txt', mode='wt', encoding='utf-8')
    # 크롬 드라이버 실행
    base_dir = os.getcwd()
    driver = webdriver.Chrome(base_dir + '/chromeforwindow')
    driver.implicitly_wait(10)
    page = 1
	# csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'hanGR1month.csv'
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

        driver.get(
            'http://english.hani.co.kr/arti/english_edition/e_northkorea/list{}.html'.format(
                page))
        result = driver.page_source
        soup = BeautifulSoup(result, 'html.parser')
        second_crawl = soup.find("ul", {"class": "list-group"}).findAll("li")

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print('http://english.hani.co.kr'+tag.get("href"))
            article_list = getText('http://english.hani.co.kr'+tag.get("href"), driver)
            #데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
            timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
            if (timestamp < criteria):
                print("시간 범위에 벗어났다")
                f.close()
                sys.exit()
            #요기에다가 mysql로 보내는 코드 작성해야합니다
            for i in article_list:
                print(i)
                print("---------------------------------------")
            wr.writerow(article_list)
            print("\n\n\n")
        page = page + 1
        print('\n****** Next page *****\n')

