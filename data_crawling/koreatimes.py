from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import time
from sshtunnel import SSHTunnelForwarder
import urllib
import sys
import MySQLdb


def getText(link,date_time):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    header = soup.find("div", {"class": "view_headline HD"})
    date = date_time
    content = soup.find("div", {"id": "startts"})
    # header = soup.find("head")
    category = 'north korea'
    author = 'null'
    print('head:',header,'date:', date, 'category',category,'author:', author,'content', content)
    print('\n\n')
    print('********')
    #
    # content_list = content_tag.findAll("div", {"class": "par"})
    # category = category_tag[0].split()[-1][9:-1]
    # author_list = author_tag[0].split()[-5:]
    # author = ""
    # for i in range(len(author_list)):
    #     if "기자" in author_list[i]:
    #         if len(author_list[i - 1]) > 6:
    #             author = author_list[i - 1][9:]
    #             break
    #         else:
    #             author = author_list[i - 2][9:]
    #             break
    #     else:
    #         author = ""
    # if "=" in author:
    #     author = author.split("=")[-1]
    #
    # content = ""
    # if (category == "연예"):
    #     for i in content_list[:-1]:
    #         content += " " + i.text.strip()
    #         content.strip()
    # else:
    #     for i in content_list:
    #         content += " " + i.text.strip()
    #         content.strip()
    #
    # header = header_tag.text.strip()
    # # 날짜 앞의 입력 스트링 제거
    # date = date_tag.text.strip()[3:19].replace(".", "-")
    #
    # return [header, date, category, author, content]




if __name__ == '__main__':
    # db=MySQLdb.connect(host="localhost", user="root",passwd="cloudera",db="mysql")
    # db.set_character_set('utf8')

    # cursor=db.cursor()
    #
    # sql="INSERT "
    d2 = date.today()
    d1 = d2 - timedelta(days=1)
    criteria = time.mktime(d1.timetuple())
    page = 1
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
            print(date_time)

            tag = i.findAll("a")[0]
            for a in tag.findAll(True):
                a.extract()
            print(tag.get("href"))
            new_tag='http://www.koreatimes.co.kr'+tag.get("href")
            print(new_tag)

            getText(new_tag,date_time)
            # 데이트가 범위 밖에 벗어나면 아예 종료 되는 부분
            # timestamp = time.mktime(datetime.strptime(article_list[1], '%Y-%m-%d %H:%M').timetuple())
            # if (timestamp < criteria):
            #     sys.exit()
            #요기에다가 mysql로 보내는 코드 작성해야합니다
            # for i in article_list:
            #     print(i)
            #     print("---------------------------------------")
            # print("\n\n\n")

        page = page + 1
        print('\n****** Next page *****\n')