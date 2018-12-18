from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
import urllib
import sys
import pymysql


def getText(link, date_time):
	req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'html.parser')

	header= soup.find("div", {"class": "view_headline HD"}).text
	
	date = date_time.strip()
	
	category = 'North Korea'
	
	author = ""
	content = ""

	try:
		content_tag = soup.find("div", {"id": "startts"}).findAll("span")
		for i in content_tag:
			content += i.text.strip() + " "
	except:
		content = soup.find("div", {"itemprop": "articleBody"}).text.strip()

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
	sql="INSERT  News_dec (article_title,article_date,article_content,article_category,article_writer,article_publisher,article_url) values (%s,%s,%s,%s,%s,%s,%s);"
	curs.execute(sql,(list[0],new_now ,list[4],list[2],list[3] ,"koreatimes",list[5]))
	conn.commit()



if __name__ == '__main__':
    # db=MySQLdb.connect(host="localhost", user="root",passwd="cloudera",db="mysql")
    # db.set_character_set('utf8')

    # cursor=db.cursor()
    #
    # sql="INSERT "
    d2 = date.today()
    d1 = d2 - timedelta(days=3650)
    criteria = time.mktime(d1.timetuple())
    page = 479
    count = 0
    while True:
        req = Request(
            "http://www.koreatimes.co.kr/www2/common/search.asp?kwd=inter-Korean&pageNum={}&pageSize=10&category=TOTAL&sort=&startDate=&endDate=&date=all&srchFd=&range=&author=all&authorData=&mysrchFd=".format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        url_collect = []
        ###Url Crawling
        second_crawl = soup.findAll("table", {"width": "100%", "border":"0","cellspacing":"0","cellpadding":"0"})[2].findAll("a")
        third_crawl = soup.findAll("table", {"width": "100%", "border":"0","cellspacing":"0","cellpadding":"0"})[2].findAll("div")
        for a, b in zip(second_crawl, third_crawl):
            print(page)
            print(count)
            date_time=b.text.strip()
            if '|' in date_time:
                date_time=date_time.split('|')[-1].strip()
                if "\n" in date_time:
                    date_time = date_time.replace("\n","")
            date_time = date_time+" 23:59"
            new_tag=a.get("href")
            print(new_tag)
            try:
                article_list = getText(new_tag,date_time)
            except:
                pass
            #데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
            timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
            if (timestamp < criteria):
                print("시간 범위에 벗어났다")
                print(count)
                sys.exit()
            count +=1
            article_list.append(new_tag)
            #요기에다가 mysql로 보내는 코드 작성해야합니다
            SQLquery(article_list)
            for i in article_list:
                print(i)
                print("———————————————————")
            print("\n\n\n")


        page = page + 1
        print('\n****** Next page *****\n')