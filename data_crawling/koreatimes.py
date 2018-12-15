from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
from datetime import date, timedelta, datetime
import time
#from sshtunnel import SSHTunnelForwarder
import urllib
import sys
#import MySQLdb
import pymysql
import json

def getText(link, date_time):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

	try:
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		header= soup.find("div", {"class": "view_headline HD"}).text
		date = date_time.strip()
		category = 'North Korea'
		author = ""
		content_tag = soup.find("div", {"id": "startts"}).findAll("span")
		content = ""
	except Exception as inst:
		print(type(inst))    # the exception instance
     	print(inst.args)     # arguments stored in .args
     	print(inst)
		bugReport(inst)
	    pass


	for i in content_tag:
		content += i.text.strip() + " "


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
		sql="INSERT  News (article_title,article_date,article_content,article_category,article_writer,article_publisher) values (%s,%s,%s,%s,%s,%s);"
		curs.execute(sql,(list[0],new_now ,list[4],list[2],list[3] ,"koreatimes"))
		conn.commit()

	except Exception as inst:
		print(type(inst))    # the exception instance
     	print(inst.args)     # arguments stored in .args
     	print(inst)
		bugReport(inst)
	    pass

def bugReport(errM,link):
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
	                    "value": "KoreaTimes",
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
    # db=MySQLdb.connect(host="localhost", user="root",passwd="cloudera",db="mysql")
    # db.set_character_set('utf8')

    # cursor=db.cursor()
    #
    # sql="INSERT "
    d2 = date.today()
    d1 = d2 - timedelta(days=90)
    criteria = time.mktime(d1.timetuple())
    page = 1
    while True:
		try:
	        req = Request(
	            "http://www.koreatimes.co.kr/www/sublist_103_{}.html".format(page))
	        webpage = urlopen(req).read()
	        soup = BeautifulSoup(webpage, 'html.parser')
	        url_collect = []
	        ###Url Crawling
	        second_crawl = soup.find("div", {"class": "section_main_left"}).findAll("div", {"class": "list_article_area"})
		except Exception as inst:
			print(type(inst))    # the exception instance
	     	print(inst.args)     # arguments stored in .args
	     	print(inst)
			bugReport(inst)
		    pass

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
			try:
	            article_list = getText(new_tag,date_time)
	            #데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
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
