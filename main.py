import requests
from bs4 import BeautifulSoup


KEYWORDS = ['Дизайн', 'фото', 'web', 'Python', 'Робототехника', 'Программирование', 'Гаджеты', 'фрагмент', 'Рождение']
LINK = 'https://habr.com/ru/all/'


def get_soup(link):
    response = requests.get(link)
    if not response.ok:
        raise ValueError('response is not valid')
    return BeautifulSoup(response.text, features='html.parser')


def get_title(artcl):
    title_elm = artcl.find('h2', class_='post__title')
    return title_elm


def get_hub(artcl):
    hub_elm = [h.text for h in artcl.find_all('a', class_='hub-link')]
    return hub_elm


def get_href(artcl):
    title = get_title(artcl)
    href = title.find('a').attrs.get('href')
    return href


def get_articles(soup, *args):
    list_of_articles = []
    for article in soup.find_all('article'):
        title = get_title(article)
        hubs = get_hub(article)
        if not args:
            source = article
        else:
            source = get_soup(get_href(article))
        for div in source.find_all('div', class_='post__text'):
            for word in KEYWORDS:
                if word in div.text or word in title.text or word in hubs:
                    list_of_articles.append(article)
    return [print_result(artcl) for artcl in set(list_of_articles)]


def print_result(artcl):
    data = artcl.find(class_='post__time')
    title = get_title(artcl)
    href = get_href(artcl)
    print(f'{data.text}{title.text}{href}\n')


if __name__ == '__main__':
    soup = get_soup(LINK)
    #Задача 1 - поиск по всей preview-информации
    get_articles(soup)
    #Задача 2 - поиск внутри статей
    get_articles(soup, 'full')