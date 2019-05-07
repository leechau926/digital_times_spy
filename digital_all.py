import requests
from bs4 import BeautifulSoup
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

def get_page_max(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html, 'lxml')
    pagenavi = soup.find(attrs={'class': 'wp-pagenavi'})
    max_page_url = pagenavi.find(attrs={'class': 'last'})['href']
    page_max = int(re.findall('/(\d+)/$', max_page_url)[0])
    return page_max

def get_item(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html, 'lxml')
    post = soup.find(attrs={'id': 'content'})
    title = post.find(attrs={'class': 'title'}).string.strip()
    if post.find(attrs={'id': 'syndication_permalink'}):
        origin_url = post.find(attrs={'id': 'syndication_permalink'}).a['href']  #ok
    else:
        origin_url = ''
    collect_date = post.find_all(attrs={'class': 'meta'})[-1].div.string.strip().split(',')[0]  #ok
    collect_time = post.find_all(attrs={'class': 'meta'})[-1].div.string.strip().split(',')[1].strip()  #ok
    categories = post.find(attrs={'class': 'category'})
    category = ''
    for itemm in categories.find_all('a'):
        category = category + itemm.string + ','
    category = category.strip(',')
    tags = post.find(attrs={'class': 'tags'}).find_all(attrs={'rel': 'tag'})
    tag = ''  #ok
    for item in tags:
        tag = tag + item.string + ','
    tag = tag.strip(',')
    entry_list = post.find(attrs={'class': 'entry'}).find_all('p')
    entry = ''  #ok
    for single in entry_list:
        if single.string:
            entry = entry + single.string + '\n'
    entry = entry.replace("'", '"')








if __name__ == '__main__':
    index_url = "https://chinadigitaltimes.net/chinese/%e6%9b%b4%e5%a4%9a%e6%96%87%e7%ab%a0/"
    page_max = get_page_max(index_url)
    print(page_max)
    # for i in range(1, page_max + 1):
    #     print('*')






