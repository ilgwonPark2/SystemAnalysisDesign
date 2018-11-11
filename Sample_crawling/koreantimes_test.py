from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
#from sshtunnel import SSHTunnelForwarder
import urllib
import sys
import csv
#import MySQLdb


def getText(link, date_time):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')

	header= soup.find("div", {"class": "view_headline HD"}).text
	
	date = date_time.strip()
	
	category = 'North Korea'
	
	author = ""
	
	content_tag = soup.find("div", {"id": "startts"}).findAll("span")
	content = ""
	
	for i in content_tag:
		content += i.text.strip() + " "
	

	return [header, date, category, author, content]





if __name__ == '__main__':
    # db=MySQLdb.connect(host="localhost", user="root",passwd="cloudera",db="mysql")
    # db.set_character_set('utf8')

    # cursor=db.cursor()
    #
    # sql="INSERT "
    d2 = date.today()
    d1 = d2 - timedelta(days=30)
    criteria = time.mktime(d1.timetuple())
    page = 1
    # csv 파일로 저장, filenmae 변수에 파일명 입력
    filename = 'koreantimes_1month.csv'
    f = open("sample_data/"+filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["제목","날짜","분류", "기자" ,"본문"])
    while True:
        req = Request(
            "http://www.koreatimes.co.kr/www/sublist_103_{}.html".format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        url_collect = []
        ###Url Crawling
        second_crawl = soup.find("div", {"class": "section_main_left"}).findAll("div", {"class": "list_article_area"})

        for i in second_crawl:
            date_time=i.findAll("div",{"class":"list_article_byline2"})[0].text
            date_time=str(date_time).split('|')[1]
            if "\n" in date_time:
                date_time = date_time.replace("\n","")
            tag = i.findAll("a")[0]
            for a in tag.findAll(True):
                a.extract()
            new_tag='http://www.koreatimes.co.kr'+tag.get("href")
            print(new_tag)

            article_list = getText(new_tag,date_time)
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