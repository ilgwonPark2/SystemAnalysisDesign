from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
from datetime import date, timedelta, datetime
import time
import urllib
import sys
import csv
import pymysql
import json

def getText(link):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	try:
		soup = BeautifulSoup(webpage, 'html.parser')
		head = soup.find("head").find("title")
		header = soup.find("h1", {"id": "news_title_text_id"}).text.strip()
		date_tag = soup.find("p", {"id": "date_text"})
		date_list = date_tag.text.strip().replace(",", "").split()

	except Exception as inst:
		print(type(inst))    # the exception instance
     	print(inst.args)     # arguments stored in .args
     	print(inst)
		print(inst)
		bugReport(inst)
	    pass

	if "January" == date_list[0]:
		date_list[0] = "01"
	elif "February" == date_list[0]:
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
	date = date_list[2] + "-" + date_list[0] + "-" + date_list[1] + " " + date_list[3]

	category = head.text.split()[-1].strip()
	try:
		author = soup.find("li", {"id": "j1"}).text.strip()
		if "By " in author:
			author = author.replace("By ", "")
	except Exception as inst:
		bugReport(inst)
		author=''
	content_tag = soup.findAll("div", {"class": "par"})
	content = ""
	for tag in content_tag:
		content_list = tag.findAll("p")
		for i in content_list:
			content += i.text.strip() + " "

	if(len(content) == 0):
		content = soup.find("div", {"class": "par"}).text.strip()


	return [header, date, category, author, content]



def SQLquery(list):   # ssh=paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('117.17.187.180',4900,'cloudera',password='cloudera')
    # print(ssh)
	try:
		conn = pymysql.connect(host='117.17.187.180', user='root',port=4100,password='cloudera',
	                           db='mysql', charset='utf8')
		curs = conn.cursor()
		now=datetime.strptime(str(article_list[1]),'%Y-%m-%d %H:%M')
		new_now=now.strftime('%Y-%m-%d %H:%M')
		sql="INSERT  News_test (article_title,article_date,artice_content,article_category,article_writer,article_publisher,article_url) values (%s,%s,%s,%s,%s,%s,%s);"
		curs.execute(sql,(list[0],new_now ,list[4],list[2],list[3] ,"chosun",list[5]))
		 #리턴값은 튜플
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
	                    "value": "Chosun",
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
    d1 = d2 - timedelta(days=1)
    criteria = time.mktime(d1.timetuple())
    page = 1
    count = 0
    while True:
		try:
	        req = Request(
	            "http://english.chosun.com/svc/list_in/search.html?query=North+Korea&pn={}".format(page))
	        webpage = urlopen(req).read()
	        soup = BeautifulSoup(webpage, 'html.parser')
	        url_collect = []
	        ###Url Crawling
	        second_crawl = soup.find("div", {"id": "list_area"}).findAll("dl", {"class": "list_item"})
		except Exception as inst:
			print(type(inst))    # the exception instance
	     	print(inst.args)     # arguments stored in .args
	     	print(inst)
			bugReport(inst)
		    pass

        print(page)
        print("\n\n\n")
        for i in second_crawl:
            tag = i.findAll("a")[0]
            for a in tag.findAll(True):
                a.extract()
            print(tag.get("href"))
            try:
                article_list = getText(tag.get("href"))
            except Exception as inst:
				bugReport(inst)
                pass
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
            count += 1
            article_list.append(tag.get("href"))
            SQLquery(article_list)
            for i in article_list:
                print(i)
                print("---------------------------------------")
            print("\n\n\n")

        page = page + 1
        print('\n****** Next page *****\n')
