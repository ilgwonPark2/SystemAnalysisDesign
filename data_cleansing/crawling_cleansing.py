# -*- coding: utf-8 -*-
import re
import pymysql


#delete null value
def deleteMissing(table,conn,curs):

   sql = "delete from " + table + " where where article_content=%s"
   curs.execute(sql, "")
   conn.commit()


#delete unrelated category contents
def deleteCategory(table,conn,curs,i):

   sql = "delete from " + table + " where article_category=%s"
   curs.execute(sql, i)
   conn.commit()


#
# def Entertainment(table,conn,curs):
#    sql = "delete from " + table + " where article_category=%s"
#    curs.execute(sql, "Entertainment")
#    conn.commit()

#delete unrelated category contents
def rmkorean(conn,curs):
   sql="SELECT id, article_content FROM News_dec_copy"
   curs.execute(sql)
   row=curs.fetchall()
   count=0
   for s in row:
      count=count+1
      id=s[0]
      s_str=str(s[1])
      hangul = re.compile('[ㄱ-ㅣ가-힣]+')
      result = hangul.sub('', s_str)
      print (result)
      print(count)
      print(id)
      print(s_str)
      sql="UPDATE News_dec_copy SET article_content=%s where id=%s"
      curs.execute(sql,(result,id))
      conn.commit()
      #result = hangul.findall(s_str)
      #print (result)

# def test2(conn, curs):
#    sql = "SELECT id,article_content FROM News_dec_copy where id=26499"
#    curs.execute(sql)
#    row = curs.fetchall()
#    count = 0
#    for s in row:
#       count = count + 1
#       id = s[0]
#       s_str = str(s[1])
#       hangul = re.compile('[ㄱ-ㅣ가-힣]+')
#       result = hangul.sub('', s_str)
#       print (result)
#       print(count)
#       print(id)
#       print(s_str)
#       sql = "UPDATE News_dec_copy SET article_content=%s where id=%s"
#       curs.execute(sql, (result, id))
#       conn.commit()
      # result = hangul.findall(s_str)
      # print (result)




if __name__ == '__main__':
   category=['Entertainment', 'Movie', 'Health', 'Travel', 'Lifestyle', 'Events', 'art&ent;', 'food', 'life']
   table="News_dec_copy"
   conn = pymysql.connect(host='117.17.187.180', user='root',port=4100,password='cloudera',
                           db='mysql', charset='utf8')
   curs = conn.cursor()
   deleteMissing(table,conn,curs)
   for i in category:
      deleteCategory(table,conn,curs,i)

   rmkorean(conn,curs)

