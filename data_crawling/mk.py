import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
from datetime import datetime
import time
import urllib
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

##selenium사용



if __name__ == '__main__':
    d2 = date.today()
    d1 = d2 - timedelta(days=1)
    criteria = time.mktime(d1.timetuple())
    #f = open('sample_nocut.txt', mode='wt', encoding='utf-8')
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

        driver.get('http://find.mk.co.kr/new/search.php?pageNum={}&cat=&cat1=&media_eco'
                   '=&pageSize=20&sub=news&dispFlag=OFF&page=news&s_kwd=%B3%B2%BA%CF&s_page=news&go_page'
                   '=&ord=1&ord1=1&ord2=0&s_keyword=%B3%B2%BA%CF&s_i_keyword=%B3%B2%BA%CF&s_author=&y1'
                   '=1991&m1=01&d1=01&y2=2018&m2=11&d2=06&ord=1&area=ttbd'.format(page))
        result = driver.page_source
        soup = BeautifulSoup(result, 'html.parser')
        second_crawl = soup.find("tr").findAll("span",{"class":"art_tit"})

        for i in second_crawl:
            tag = i.findAll("a")[0]
            print(tag.get("href"))

        page = page + 1
        print('\n****** Next page *****\n')
	# f.close()






