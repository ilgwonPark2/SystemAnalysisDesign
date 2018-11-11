from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
from sshtunnel import SSHTunnelForwarder
import urllib
import sys
import MySQLdb
from selenium import webdriver
import os
#





if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=30)
    criteria = time.mktime(d1.timetuple())
    # f = open('sample_nocut.txt', mode='wt', encoding='utf-8')
    # 크롬 드라이버 실행
    base_dir = os.getcwd()
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

        driver.get(
            'http://english.hani.co.kr/arti/english_edition/e_northkorea/list{}.html'.format(
                page))
        result = driver.page_source
        soup = BeautifulSoup(result, 'html.parser')
        second_crawl = soup.find("ul", {"class": "list-group"}).findAll("li")

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print('http://english.hani.co.kr'+tag.get("href"))
           # article_list = getText('http://english.hani.co.kr'+tag.get("href"))
            # 데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
            #timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
        #     if (timestamp < criteria):
        #         sys.exit()
        # # 요기에다가 mysql로 보내는 코드 작성해야합니다
        # for i in article_list:
        #     print(i)
        #     print("---------------------------------------")
        #     print("\n\n\n")
        page = page + 1
        print('\n****** Next page *****\n')

