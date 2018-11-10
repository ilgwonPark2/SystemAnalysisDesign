import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey='6LtKXgn8XiDZCjAOgr6ibyiyO8yYOXXdwcu4cwKxVUHc',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

_text = """A long-simmering issue has risen to the surface with the announcement by the Japanese Maritime Self Defense Force (MSDF) of its plan to fly the Rising Sun Flag over its warships during an international naval review set to take place on Jeju Island.\"Japan must delicately consider the effect that Rising Sun Flag has on the Korean people,\" said South Korean Prime Minister Lee Nak-yeon on Oct. 1.
The MSDF’s plan to raise the flag, which has become a symbol of Japanese aggression during World War II, run counter to the Republic of Korea Navy and Foreign Ministry’s request that participating countries fly only their own national flag and the South Korean flag, and Lee is clearly calling for restraint.There have been calls in certain political circles to demand that Japanese participation in the naval review be disallowed, but Lee simply said, \"We are considering various responses.\"Ramifications to South Korea-Japanese relations are being evaluated.It is international custom to consider the views of the host country during a naval review, and it would be appropriate for the Japanese government to consider the sentiment of the Korean people by not flying the Rising Sun flag.\“The Rising Sun flag is the ensign of the Japanese Navy, and raising it is a domestic statutory obligation,\" said a spokesman for the Japanese government, who termed the request to refrain from flying it, \"a discourteous action.\" Yet this is simply a case of a false victimization.
The Japanese Navy first used the Rising Sun flag in 1870, and it was the flag that Japan used when it started the Pacific War and invaded countries throughout Asia. The flag itself symbolizes Japanese belligerence. It is for this reason that neighboring countries such as South Korea and China object to the raising of the flag.
Nevertheless, the MSDF continues to use a 16-ray Rising Sun Flag, while the Ground Self Defense Force uses an eight-ray flag. Such flagrant acts are a denial of Japan’s past history as an invading and criminal nation.
Section 86 of the German criminal code provides for fines and/or a prison sentence of up to three years for, \"using or distributing flags, uniforms, badges, or slogans that symbolize the Nazis,\" and also contains provisions banning the use of twisted crosses such as the Häcken Kreitz.
In viewing the MSDF’s stubborn insistence on flying the Rising Sun Flag along with Japanese Prime Minister Shinzo Abe’s drive to reform the pacifist constitution, there are concerns within the international community that Japanese militarism is undergoing a revival. If Japan wants true peace, it needs to come to its own decision for lowering the flag."""

response = natural_language_understanding.analyze(
    text=_text,
    features=Features(sentiment=SentimentOptions(targets=['japan']))).get_result()

print(json.dumps(response, indent=2))
