import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

url = 'https://chinadigitaltimes.net/recent-stories/page/'
f = open('output.txt', 'a', encoding='utf-8')

def get_item(page_num):
    page_url = url + str(page_num) + '/'
    html = requests.get(page_url, headers=headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.content, 'lxml')
    contents = soup.find_all(attrs={'class': 'st-related-posts'})
    lists = contents[0].find_all('li')
    for list in lists:
        date = list.find(attrs={'class': 'related_date'}).string
        title = list.a['title']
        pas_url = list.a['href']
        f.write('%s, %s, %s\n' % (date, title, pas_url))
    print('page %d saved!' % page_num)

if __name__ == '__main__':
    pool = Pool(2)
    pool.map(get_item, [i for i in range(1,114)])
