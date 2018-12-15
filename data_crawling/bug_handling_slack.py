from urllib import request, parse
import json

post = {
    "attachments": [
        {
            "text": "<http://news.donga.com/3/all/20180523/90199081/1|Donga> - This link makes crawling error",
            "fields": [
                {
                    "title": "Part",
                    "value": "Data Crawling",
                    "short": True
                },
                {
                    "title": "NewsPaper",
                    "value": "Donga",
                    "short": True
                },
                 {
                    "title": "Priority",
                    "value": "High",
                    "short": False
                }
            ],
            "color": "danger",
            "footer": "Emma, Daniel",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts":1541395367
        }
    ]
}

json_data = json.dumps(post)
req = request.Request("https://hooks.slack.com/services/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", data=json_data.encode('ascii'), headers={'Content-Type': 'application/json'})
resp = request.urlopen(req)
