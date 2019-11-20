from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

data = [
    ['https://lenta.ru', 'h1.b-topic__title', 'p'],
    ['https://russian.rt.com', 'h1.article__heading', 'div.article__text']
]


class WebBot:
    def get_page(self, url):
        try:
            req = requests.get(url)
        except:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def get_data(self, obj, selector):
        elements = obj.select(selector)
        if elements is not None and len(elements) > 0:
            return '\n'.join([element.text for element in elements])
        return 'anyerr'

    def parse(self, site, url):
        full_path = site.url + url
        bs = get_page(full_path)
        if bs is not None:
            title = self.get_data(bs, site.title)
            body = self.get_data(bs, site.body)
            if title != '' and body != '':
                content = Content(full_path, title, body)
                content.show()





class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def show(self):
        print(self.title)
        print(self.url)
        print(self.body)


def news_from_lenta(url):
    bs = get_page(url)
    if bs is None:
        return bs
    title = bs.find('h1', {'class': 'b-topic__title'}).text
    lines = bs.find_all('p')
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)


def news_from_rt(url):
    bs = get_page(url)
    if bs is None:
        return bs
    title = bs.find('h1', {'class': 'article__heading'}).text
    lines = bs.find_all('div', {'class': 'article__text'})
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)





def get_page(url):
    req = requests.get(url)
    if req.status_code == 200:
        return BeautifulSoup(req.text, 'html.parser')
    return None

class Site:
    def __init__(self, host, title_tag, body_tag):
        self.url = host
        self.title = title_tag
        self.body = body_tag

sites = []
for item in data:
    sites.append(Site(item[0], item[1], item[2]))


bot = WebBot()
bot.parse(sites[0], '/news/2019/11/19/ohmygod/')
bot.parse(sites[0], '/nopolitics/article/688503-pogoda-holod-nachalo-zima')