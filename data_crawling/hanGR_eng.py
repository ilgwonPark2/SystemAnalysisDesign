from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
from datetime import date, timedelta, datetime
import time
import urllib
import sys
from selenium import webdriver
import os
import pymysql
import json

def getText(link, driver):
	driver.get(link)
	result = driver.page_source
	try:
		soup = BeautifulSoup(result, 'html.parser')
		header= soup.find("h2", {"id": "titleapp"}).find("div").text.strip()
		date_list = soup.find("div", {"class": "headline-data"}).text.strip().split("KST")[0][12:].split()
		hour = date_list[-1]
		rest = date_list[0].split(".")
		month = rest[0]
		day = rest[1].split(",")[0]
		year = rest[1].split(",")[-1]
	except Exception as inst:
		print(type(inst))    # the exception instance
     	print(inst.args)     # arguments stored in .args
     	print(inst)
		bugReport(inst)
	    pass

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
	except Exception as inst:
		bugReport(inst)
		author= ""


	return [header, date, category, author, content]


def SQLquery(list):
	try:
		conn = pymysql.connect(host='117.17.187.180', user='root',port=4100,password='cloudera',
	                           db='mysql', charset='utf8')
		curs = conn.cursor()
		now=datetime.strptime(str(article_list[1]),'%Y-%m-%d %H:%M')
		new_now=now.strftime('%Y-%m-%d %H:%M')
		sql="INSERT  News (article_title,article_date,article_content,article_category,article_writer,article_publisher) values (%s,%s,%s,%s,%s,%s);"
		curs.execute(sql,(list[0],new_now ,list[4],list[2],list[3] ,"hangyeorye"))
		conn.commit()

	except Exception as inst:
		print(type(inst))    # the exception instance
     	print(inst.args)     # arguments stored in .args
     	print(inst)
		bugReport(inst)
	    pass


def bugReport(errM):
	post = {
	    "attachments": [
	        {
	            "text": link +  "  " + errM,
	            "fields": [
	                {
	                    "title": "Part",
	                    "value": "Data Crawling",
	                    "short": True
	                },
	                {
	                    "title": "NewsPaper",
	                    "value": "Hangyeorye",
	                    "short": True
	                },
	                 {
	                    "title": "Priority",
	                    "value": "High",
	                    "short": False
	                }
	            ],
	            "color": "danger",
	            "footer": "Emma, Daniel",
	            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
	            "ts":1541395367
	        }
	    ]
	}
	json_data = json.dumps(post)
	req = request.Request("https://hooks.slack.com/services/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", data=json_data.encode('ascii'), headers={'Content-Type': 'application/json'})
	resp = request.urlopen(req)



if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=90)
    criteria = time.mktime(d1.timetuple())
    # 크롬 드라이버 실행
    base_dir = os.getcwd()
	# if you use window os, change the '/chromedriver' -> '/chromeforwindow.exe'
    driver = webdriver.Chrome(base_dir + '/chromedriver')
    driver.implicitly_wait(10)
    page = 1
    while True:
        # session = requests.Session()
        # session.headers.update({'User-Agent': 'Custom user agent'})
        #
        #
        # headers=session.get('http://www.nocutnews.co.kr/headers')
        # print(headers)
		try:
	        driver.get(
	            'http://english.hani.co.kr/arti/english_edition/e_northkorea/list{}.html'.format(
	                page))
	        result = driver.page_source
	        soup = BeautifulSoup(result, 'html.parser')
	        second_crawl = soup.find("ul", {"class": "list-group"}).findAll("li")
		except Exception as inst:
			print(type(inst))    # the exception instance
	     	print(inst.args)     # arguments stored in .args
	     	print(inst)
			bugReport(inst)
		    pass

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print('http://english.hani.co.kr'+tag.get("href"))
			try:
	            article_list = getText('http://english.hani.co.kr'+tag.get("href"), driver)
				try:
		            #데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
		            timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
				except Exception as inst:
		            if (timestamp < criteria):
		                print("시간 범위에 벗어났다")
		                sys.exit()
					print(type(inst))    # the exception instance
			     	print(inst.args)     # arguments stored in .args
			     	print(inst)
					bugReport(inst)
				    pass
            	#요기에다가 mysql로 보내는 코드 작성해야합니다
	            SQLquery(article_list)
			    for i in article_list:
					print(i)
					print("---------------------------------------")
				print("\n\n\n")
			except Exception as inst:
				bugReport(inst,page)
				pass

	        page = page + 1
        print('\n****** Next page *****\n')
