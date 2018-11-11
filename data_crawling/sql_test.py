import MySQLdb
from sshtunnel import SSHTunnelForwarder
import paramiko
import

# server = SSHTunnelForwarder(
#     ('117.17.187.180',4900),
#     ssh_username="cloudera",
#     ssh_password="cloudera",
#     remote_bind_address=('117.17.187.180',3306)
# )
#
# server.start()
# print('start complete')
# print(server._remote_binds)
# print(server.local_bind_host)# show assigned local port
# # work with `SECRET SERVICE` through `server.local_bind_port`.
# conn = MySQLdb.connect(host='127.0.0.1',
#                        port=server.local_bind_port,
#                        user='root',
#                        passwd='Cloudera301!',
#                        db='mysql')
# # config = {
# #   'user': 'root',
# #   'password': 'cloudera',
# #   'host': '127.0.0.1',
# #   'database': 'mysql',
# # }
#
# conn = MySQLdb.connect(conn)
# conn.set_character_set('utf8')
# cursor=conn.cursor()
# print("process")
# sql="select * from News;"
# cursor.execute(sql)
# conn.commit()
#
#
#
# server.stop()
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
def getText('', date_time):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    header = soup.find("div", {"class": "view_headline HD"}).text

    date = date_time.strip()

    category = 'North Korea'

    author = ""

    content_tag = soup.find("div", {"id": "startts"}).findAll("span")
    content = ""

    for i in content_tag:
        content += i.text.strip() + " "

    return [header, date, category, author, content]



# import pymysql
#
# def SQL_text():
#     # ssh=paramiko.SSHClient()
#     # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     # ssh.connect('117.17.187.180',4900,'cloudera',password='cloudera')
#     # print(ssh)
#     conn = pymysql.connect(host='117.17.187.180', user='root',port=4100,password='cloudera',
#                            db='mysql', charset='utf8')
#     sql = "INSERT INTO News Values(%s,%s,%s,%s,%s,%s)"
#     curs.execute(sql, (list[0], new_now, list[4], list[2], list[3], "chosun"))
#     print(curs.execute(sql))  # 리턴값은 튜플
#     conn.commit()
#
#     # curs = conn.cursor()
#     # sql="select * from test;"
#     # print(curs.execute(sql)) #리턴값은 튜플
#     # conn.commit()
#
#
# SQL_text()