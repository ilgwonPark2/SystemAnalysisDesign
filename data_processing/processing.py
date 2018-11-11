import MySQLdb
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions, KeywordsOptions




def initDB():
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='cloudera', db='mysql')
    return conn.cursor()

def updateDB(_cursor,_content, _id):
    # inserting
    # sql="insert News_copy(article_title,article_date,article_content,article_category,article_writer,article_publisher,article_analysis) VALUES (%s, %s, %s,%s,%s,%s,%s);"
    # cursor.execute(sql, ('Parkilgwon', '2018-10-22', 'abc', 'category', 'writer', 'pulisher', json.dumps(response, indent=2)))
    sql= "UPDATE News_copy SET article_analysis = %s WHERE id = %s;"
    # if executing succed, it returns 1(True), or 0(False)
    sql_return = cursor.execute(sql, [_content,_id])
    if sql_return == 1:
        conn.commit()
    return (sql_return == 1)

def countRow(_cursor):
    sql= "SELECT id, article_content FROM News;"
    sql_return = cursor.execute(sql)
    result = cursor.fetchall()
    return (sql_return)



def doNLP(_content):
    _token=['6LtKXgn8XiDZCjAOgr6ibyiyO8yYOXXdwcu4cwKxVUHc','RAXTXY4DOozh-zWFV71yhhJxEP3QIDRNUClfIupJdslC']
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        iam_apikey=_token[0],
        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
        )

    response = natural_language_understanding.analyze(
        text=_content,
        features=Features(sentiment=SentimentOptions(),emotion=EmotionOptions(),keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()

    print(json.dumps(response, indent=2))

    return json.dumps(response, indent=2)

if __name__ == '__main__':
    cursor = initDB()


# document reference
# https://console.bluemix.net/apidocs/natural-language-understanding?language=python#emotion


# test data
_text = """A long-simmering issue has risen to the surface with the announcement by the Japanese Maritime Self Defense Force (MSDF) of its plan to fly the Rising Sun Flag over its warships during an international naval review set to take place on Jeju Island.\"Japan must delicately consider the effect that Rising Sun Flag has on the Korean people,\" said South Korean Prime Minister Lee Nak-yeon on Oct. 1.
The MSDF’s plan to raise the flag, which has become a symbol of Japanese aggression during World War II, run counter to the Republic of Korea Navy and Foreign Ministry’s request that participating countries fly only their own national flag and the South Korean flag, and Lee is clearly calling for restraint.There have been calls in certain political circles to demand that Japanese participation in the naval review be disallowed, but Lee simply said, \"We are considering various responses.\"Ramifications to South Korea-Japanese relations are being evaluated.It is international custom to consider the views of the host country during a naval review, and it would be appropriate for the Japanese government to consider the sentiment of the Korean people by not flying the Rising Sun flag.\“The Rising Sun flag is the ensign of the Japanese Navy, and raising it is a domestic statutory obligation,\" said a spokesman for the Japanese government, who termed the request to refrain from flying it, \"a discourteous action.\" Yet this is simply a case of a false victimization.
The Japanese Navy first used the Rising Sun flag in 1870, and it was the flag that Japan used when it started the Pacific War and invaded countries throughout Asia. The flag itself symbolizes Japanese belligerence. It is for this reason that neighboring countries such as South Korea and China object to the raising of the flag.
Nevertheless, the MSDF continues to use a 16-ray Rising Sun Flag, while the Ground Self Defense Force uses an eight-ray flag. Such flagrant acts are a denial of Japan’s past history as an invading and criminal nation.
Section 86 of the German criminal code provides for fines and/or a prison sentence of up to three years for, \"using or distributing flags, uniforms, badges, or slogans that symbolize the Nazis,\" and also contains provisions banning the use of twisted crosses such as the Häcken Kreitz.
In viewing the MSDF’s stubborn insistence on flying the Rising Sun Flag along with Japanese Prime Minister Shinzo Abe’s drive to reform the pacifist constitution, there are concerns within the international community that Japanese militarism is undergoing a revival. If Japan wants true peace, it needs to come to its own decision for lowering the flag."""
