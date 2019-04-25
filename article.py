import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

def get_item(text):
    # html = requests.get(url, headers=headers)
    # html.encoding = 'utf-8'
    soup = BeautifulSoup(text, 'lxml')
    post = soup.find(attrs={'id': 'content'})
    title = post.find(attrs={'class': 'title'}).string.strip()  #ok
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
    insert_sql = """INSERT INTO articles (title, origin_url, collect_date, collect_time, category, tag, entry) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');\n""" % (title, origin_url, collect_date, collect_time, category, tag, entry)
    with open('insertsql.sql', 'a', encoding='utf-8') as writesql:
        writesql.write(insert_sql)
    print('Article "%s" saved!' % title)


if __name__ == '__main__':
    r = open('urls.txt', 'r', encoding='utf-8')
    for url in r.readlines():
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        text = response.content
        get_item(text)

"""
TABLE articles CREATE SQL:
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `origin_url` longtext,
  `collect_date` varchar(45) DEFAULT NULL,
  `collect_time` varchar(45) DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL,
  `tag` varchar(200) DEFAULT NULL,
  `entry` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
"""
