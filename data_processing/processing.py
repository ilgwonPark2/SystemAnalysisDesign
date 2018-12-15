import MySQLdb
import json
import time
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions, KeywordsOptions


def initDB():
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='cloudera', db='mysql')
    return conn

def updateDB(_conn, _content, _id):
    # inserting
    # sql="insert News_copy(article_title,article_date,article_content,article_category,article_writer,article_publisher,article_analysis) VALUES (%s, %s, %s,%s,%s,%s,%s);"
    # cursor.execute(sql, ('Parkilgwon', '2018-10-22', 'abc', 'category', 'writer', 'pulisher', json.dumps(response, indent=2)))
    sql= "UPDATE News_dec_copy SET article_analysis = %s WHERE id = %s;"
    # if executing succed, it returns 1(True), or 0(False)
    sql_return = _conn.cursor().execute(sql, [_content, _id])
    if sql_return == 1:
        _conn.commit()
    return (sql_return == 1)

def selectDB(_conn):
    _cursor = _conn.cursor()
    sql = "SELECT id, article_content FROM News_dec_copy;"
    sql_return = _cursor.execute(sql)
    result = _cursor.fetchall()
    return result

def doNLP(_content):
    # Use your own IBM token (replace fake_tokens)
    _token = ['RAXTXY4DOozh-zWFV71yhhJxEP3QIDRNUClfIupJdslC','fake_token2','fake_token3','fake_token4']
    # _token_limit = True
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        iam_apikey=_token[0],
        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
        )
    try:
        response = natural_language_understanding.analyze(
            text=_content,
            features=Features(sentiment=SentimentOptions(),emotion=EmotionOptions(),keywords=KeywordsOptions(sentiment=True,emotion=True,limit=3)))
        if response.get_status_code() != 200:
            raise Exception
        _nlp_result = json.dumps(response.get_result(), indent=2)
        _nlp_processed = processNLP(_nlp_result)
        # print(response.get_headers())
        # print(response.get_status_code())
    except Exception as e:
        print(e)
        print(e.args)
        _nlp_processed = '{"result":"unsupported language"}'
        return _nlp_processed
    else:
        return _nlp_processed

def processNLP(_nlp_result):
    tmp = json.loads(_nlp_result)
    for x in range(len(tmp['keywords'])):
        str_key ='keyword'+str(x+1)
        if tmp['keywords'][x] != '':
            tmp[str_key] = tmp['keywords'][x]
        else:
            tmp[str_key] = ''
    tmp.pop('keywords')
    _nlp_processed = json.dumps(tmp, indent=2)
    # print(_nlp_processed)
    return _nlp_processed


if __name__ == '__main__':
    conn = initDB()
    sql_return = selectDB(conn)
    _cursor = conn.cursor()
    # print(sql_return)
    for row in sql_return:
        if row[1].strip() != '':
            json_data = doNLP(row[1])
            time.sleep(0.1)
            print(row[0],json_data)
            updateDB(conn, json_data, row[0])

    print('------------------------------------------------')
    print('------------------------------------------------')
    print('Finished')
    print('------------------------------------------------')
    print('------------------------------------------------')



#
#
# # document reference
# # https://console.bluemix.net/apidocs/natural-language-understanding?language=python#emotion
#
#
#
# # Counting progress from MySQLdb
# mysql> select count(article_analysis) from News_interim;
# +-------------------------+
# | count(article_analysis) |
# +-------------------------+
# |                     274 |
# +-------------------------+
# 1 row in set (0.00 sec)
#
#
#
# # test data
# _text = """A long-simmering issue has risen to the surface with the announcement by the Japanese Maritime Self Defense Force (MSDF) of its plan to fly the Rising Sun Flag over its warships during an international naval review set to take place on Jeju Island.\"Japan must delicately consider the effect that Rising Sun Flag has on the Korean people,\" said South Korean Prime Minister Lee Nak-yeon on Oct. 1.
# The MSDF’s plan to raise the flag, which has become a symbol of Japanese aggression during World War II, run counter to the Republic of Korea Navy and Foreign Ministry’s request that participating countries fly only their own national flag and the South Korean flag, and Lee is clearly calling for restraint.There have been calls in certain political circles to demand that Japanese participation in the naval review be disallowed, but Lee simply said, \"We are considering various
#responses.\"Ramifications to South Korea-Japanese relations are being evaluated.It is international custom to consider the views of the host country during a naval review, and it would be appropriate for the Japanese government to consider the sentiment of the Korean people by not flying the Rising Sun flag.\“The Rising Sun flag is the ensign of the Japanese Navy, and raising it is a domestic statutory obligation,\" said a spokesman for the Japanese government, who termed the request to refrain from flying it, \"a discourteous action.\" Yet this is simply a case of a false victimization.
# The Japanese Navy first used the Rising Sun flag in 1870, and it was the flag that Japan used when it started the Pacific War and invaded countries throughout Asia. The flag itself symbolizes Japanese belligerence. It is for this reason that neighboring countries such as South Korea and China object to the raising of the flag.
# Nevertheless, the MSDF continues to use a 16-ray Rising Sun Flag, while the Ground Self Defense Force uses an eight-ray flag. Such flagrant acts are a denial of Japan’s past history as an invading and criminal nation.
# Section 86 of the German criminal code provides for fines and/or a prison sentence of up to three years for, \"using or distributing flags, uniforms, badges, or slogans that symbolize the Nazis,\" and also contains provisions banning the use of twisted crosses such as the Häcken Kreitz.
# In viewing the MSDF’s stubborn insistence on flying the Rising Sun Flag along with Japanese Prime Minister Shinzo Abe’s drive to reform the pacifist constitution, there are concerns within the international community that Japanese militarism is undergoing a revival. If Japan wants true peace, it needs to come to its own decision for lowering the flag."""
