# @Author: Michael
# comments.py
# 2017/10/2 18:06
import requests
import bs4
import random
import pymongo
from time import sleep
from get_cookie import *
base_url = 'https://movie.douban.com/subject/26705541/comments'

comment_url = 'https://movie.douban.com/subject/26705541/comments?start=0&limit=20&sort=new_score&status=P'

headers_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


IP = 'localhost'
PORT = 27017
DATABASE_NAME = 'douban'
COLLECTIONS_NAME = 'comments'
douban_cookies = get_cookie_from_chrome(host='.douban.com')
movie_douban_cookies = get_cookie_from_chrome(host='movie.douban.com')
cookies = dict(douban_cookies, **movie_douban_cookies)
URL_HISTTORY = set()

def parse_html(url, base_url=base_url, headers=headers_agent):
    print('[url]: {}'.format(url))
    if url in URL_HISTTORY:
        return None
    resp = requests.get(url=url, headers=headers, cookies=cookies)
    if resp.status_code == 403:
        print('【url】: 拒绝访问--{}'.format(url))
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    next_url = soup.find(id='paginator').find(class_='next')['href']
    items = soup.find(id='comments').find_all(class_='comment-item')
    with pymongo.MongoClient(host=IP, port=PORT) as f:
        db = f[DATABASE_NAME]
        collection = db[COLLECTIONS_NAME]
        for item in items:
            data = get_data(item)
            # filters = {'comments_text': data['comment_text']}
            # if collection.find(filters):
            #     collection.update(data, filters)
            collection.insert(data)
    sleep(random.random() + 3)
    URL_HISTTORY.add(url)
    return parse_html(url=base_url + next_url) if next_url else None

def get_data(item=None):
    avator = item.find(class_='avatar')
    # name = avator.find('a')['title']
    comment = item.find(class_='comment')
    commenter_url = avator.find('a')['href']
    comment_vote = comment.find(class_='comment-vote')
    vote = int(comment_vote.find(class_='votes').text)
    vote_info = comment_vote.find('a').text.strip()
    comment_info = comment.find(class_='comment-info')
    name = comment_info.find('a').text.strip()
    spans = comment_info.find_all('span')
    is_read = spans[0].text.strip()
    star = spans[1]['class'][0][-2]
    star_text = spans[1]['title']
    comment_time = spans[-1]['title']
    comment_text = comment.find('p').text.strip()
    return {
        'name': name,
        'commenter_url': commenter_url,
        'vote': vote,
        'vote_info': vote_info,
        'is_read': is_read,
        'star': star,
        'star_text': star_text,
        'comment_time': comment_time,
        'comment_text': comment_text
    }

if __name__ == '__main__':
    parse_html(url=comment_url)