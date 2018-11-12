from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
from selenium import webdriver
import time
import os
#from sshtunnel import SSHTunnelForwarder
import pymysql
import sys
#import MySQLdb


def getText(link, driver):
	driver.get(link)
	result = driver.page_source
	soup = BeautifulSoup(result, 'html.parser')


	header= soup.find("h3", {"id": "sTitle_a"}).text.strip()

	date_tag = soup.find("span", {"class": "date"})
	date_list = date_tag.text.strip().replace(","," ").split()
	if "Jan" == date_list[0]:
		date_list[0] = "01"
	elif "Feb" == date_list[0]:
		date_list[0] = "02"
	elif "Mar" == date_list[0]:
		date_list[0] = "03"
	elif "Apr" == date_list[0]:
		date_list[0] = "04"
	elif "May" == date_list[0]:
		date_list[0] = "05"
	elif "Jun" == date_list[0]:
		date_list[0] = "06"
	elif "Jul" == date_list[0]:
		date_list[0] = "07"
	elif "Aug" == date_list[0]:
		date_list[0] = "08"
	elif "Sep" == date_list[0]:
		date_list[0] = "09"
	elif "Oct" == date_list[0]:
		date_list[0] = "10"
	elif "Nov" == date_list[0]:
		date_list[0] = "11"
	elif "Dec" == date_list[0]:
		date_list[0] = "12"
	date = date_list[2]+"-"+date_list[0]+"-"+date_list[1]+" 12:00"

	category = soup.find("li", {"class": "on"}).find("a").find("span").text.strip()

	content_tag = soup.find("div", {"id": "articlebody"})

	for i in content_tag:
		i.extract()
	content = content_tag.text.strip()
	if "이미지뷰" in content:
		content = content.replace("이미지뷰", "")

	try:
		author = str(content).split('BY')[1].strip()
		if "[" in author:
			author = author.split("[")[0].strip()
	except:
		author=""


	return [header, date, category, author, content]

def SQLquery(list):   # ssh=paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('117.17.187.180',4900,'cloudera',password='cloudera')
    # print(ssh)
	conn = pymysql.connect(host='117.17.187.180', user='root',port=4100,password='cloudera',
                           db='mysql', charset='utf8')
	curs = conn.cursor()
	now=datetime.strptime(str(article_list[1]),'%Y-%m-%d %H:%M')
	new_now=now.strftime('%Y-%m-%d %H:%M')
	sql="INSERT  News (article_title,article_date,article_content,article_category,article_writer,article_publisher) values (%s,%s,%s,%s,%s,%s);"
	curs.execute(sql,(list[0],new_now ,list[4],list[2],list[3] ,"joongang"))
	conn.commit()

if __name__ == '__main__':
	d2 = date.today()
	d1 = d2 - timedelta(days=90)
	criteria = time.mktime(d1.timetuple())
	page = 1
	base_dir = os.getcwd()
	driver = webdriver.Chrome(base_dir + '/chromedriver')
	driver.implicitly_wait(10)
	while True:
		req = Request("http://koreajoongangdaily.joins.com/search/search.aspx?sw=north+korea&x=18&y=16&pgi={}".format(page))
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		url_collect = []
		###Url Crawling
		second_crawl = soup.find("div", {"id": "news_list"}).findAll("li")
		for i in second_crawl:
			tag = i.findAll("a")[0]
			for a in tag.findAll(True):
				a.extract()
			print(tag.get("href"))
			new_tag=tag.get("href").split('&query')[0]
			try:
				article_list = getText(new_tag, driver)
			#데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
				timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
				if (timestamp < criteria):
					print("시간 범위에 벗어났다")
					sys.exit()
			#요기에다가 mysql로 보내는 코드 작성해야합니다
			#SQLquery(article_list)
				SQLquery(article_list)
				for i in article_list:
					print(i)
					print("---------------------------------------")
				print("\n\n\n")
			except:
				pass
		print(page)
		page = page + 1
		print('\n****** Next page *****\n')