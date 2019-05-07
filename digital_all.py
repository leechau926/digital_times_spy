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









if __name__ == '__main__':
    index_url = "https://chinadigitaltimes.net/chinese/%e6%9b%b4%e5%a4%9a%e6%96%87%e7%ab%a0/"






