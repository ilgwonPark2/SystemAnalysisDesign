from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys
import MySQLdb
import pymysql

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
    # db=MySQLdb.connect(host="localhost", user="root",passwd="cloudera",db="mysql")
    # db.set_character_set('utf8')

    # cursor=db.cursor()
    #
    # sql="INSERT "
    d2 = date.today()
    d1 = d2 - timedelta(days=30)
    criteria = time.mktime(d1.timetuple())
    page = 1
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
                sys.exit()
            db=pymysql.connect(host='117.17.187.180',port=4100, user='root',password='Cloudera301!',db='mysql')
            db.set_character_set('utf8')
            cursor=db.cursor()
            sql = "INSERT INTO News Values(%s,%s,%s,%s,%s)" % (
            "'" + article_list[0] + "'", "'" + article_list[1] + "'", "'" + article_list[2] + "'",
            "'" + article_list[3] + "'", "'" + article_list[4] + "'", "'" + "chosun" + "'")
            for i in article_list:
                print(i)
                print("---------------------------------------")
            print("\n\n\n")
            
        page = page + 1
        print('\n****** Next page *****\n')