import os
import random
import time

from bs4 import BeautifulSoup
import requests


cookies = dict([a.split('=', 1) for a in """cookies from browser""".split(';')])
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

topics = {
    19551556: "旅行",
    19789286: "日语学习",
    19562563: "日剧",
    19860581: "JLPT",
    19622153: "留学日本",
    19550994: "游戏",
    19597091: "日本文学",
    19591985: "动漫"
}

top_url = 'https://www.zhihu.com/topic/%s/top-answers?page=%s'


def crawl_topic_top_answers(topic_id, name):
    filepath = name + '.txt'
    if os.path.exists(filepath):
        return

    contents = []
    for page in range(1, 11):
        url = top_url % (topic_id, page)
        print('crawl url: ', url)
        res = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(res.content, "lxml")
        for item in soup.find_all(class_="feed-item"):
            title = item.find("a", class_="question_link").text
            summary = item.find(class_="summary").text.replace("显示全部", "")
            contents.append("%s\n%s" % (title.strip(), summary.strip()))

    with open(filepath, 'w') as f:
        f.write('\n\n'.join(contents))

for topic_id, name in topics.items():
    crawl_topic_top_answers(topic_id, name)
    print('sleeping for next task...')
    time.sleep(random.randint(30, 100))
