from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
from datetime import datetime
import time
import urllib
import sys









if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=1)
    criteria = time.mktime(d1.timetuple())
    f = open('sample_hankyung.txt', mode='wt', encoding='utf-8')
    page = 1
    while True:
        req = Request('http://search.hankyung.com/apps.frm/search.news?query='
                      '%EB%82%A8%EB%B6%81&mediaid_clust=HKPAPER,HKCOM&page={}'.format(page))
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
		###Url Crawling
        second_crawl=soup.find("ul",{"class":"article"}).findAll("li")

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print(tag.get("href"))
			# header, date, content = getText(tag.get("href"))
			# f.write(header + '\t' + date + '\t' + content + '\n')
			# # # 데이트가 범위 밖에 벗어나면 아예 종료 되는 코드 여기에 작성
			# timestamp = time.mktime(datetime.strptime(date, '%Y-%m-%d %H:%M').timetuple())
			# if (timestamp < criteria):
			# 	sys.exit()

        page = page + 1
        print('\n****** Next page *****\n')