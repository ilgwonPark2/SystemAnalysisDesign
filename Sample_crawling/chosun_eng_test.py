from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys
import csv
#import MySQLdb

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')

	header= soup.find("h1", {"id": "news_title_text_id"}).text.strip()
	
	date_tag = soup.find("p", {"id": "date_text"})
	date_list = date_tag.text.strip().replace(",","").split()
	if "January" == date_list[0]:
		date_list[0] = "01"
	elif "Feburary" == date_list[0]:
		date_list[0] = "02"
	elif "March" == date_list[0]:
		date_list[0] = "03"
	elif "April" == date_list[0]:
		date_list[0] = "04"
	elif "May" == date_list[0]:
		date_list[0] = "05"
	elif "June" == date_list[0]:
		date_list[0] = "06"
	elif "July" == date_list[0]:
		date_list[0] = "07"
	elif "August" == date_list[0]:
		date_list[0] = "08"
	elif "September" == date_list[0]:
		date_list[0] = "09"
	elif "October" == date_list[0]:
		date_list[0] = "10"
	elif "November" == date_list[0]:
		date_list[0] = "11"
	elif "December" == date_list[0]:
		date_list[0] = "12"
	date = date_list[2]+"-"+date_list[0]+"-"+date_list[1]+" "+date_list[3]
	
	category = 'north korea'
	
	author = soup.find("li",{"id":"j1"}).text.strip()
	if "By " in author:
		author = author.replace("By ", "")
	
	content_tag = soup.find("div", {"class": "par"}).findAll("p")
	content = ""
	
	for i in content_tag:
		content += i.text.strip() + " "
	

	return [header, date, category, author, content]



if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=30)
    criteria = time.mktime(d1.timetuple())
    page = 1
    # csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'chosun_1day.csv'
    f = open("sample_data/"+filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["제목","날짜","분류", "기자" ,"본문"])
    while True:
        req = Request(
            "http://english.chosun.com/svc/list_in/list.html?catid=F&pn={}".format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        url_collect = []
        ###Url Crawling
        second_crawl = soup.find("div", {"id": "list_area"}).findAll("dl", {"class": "list_item"})

        for i in second_crawl:
            tag = i.findAll("a")[0]
            for a in tag.findAll(True):
                a.extract()
            print('http://english.chosun.com/'+tag.get("href"))
            
            article_list = getText('http://english.chosun.com/'+tag.get("href"))
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