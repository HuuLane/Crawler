from pyquery import PyQuery as pq
import requests
import logging
log = logging.getLogger('root')


def cached_url(url):
    """
    cache the url
    """
    import os
    folder = 'cached'
    # https://maoyan.com/board -> board.html
    filename = url.rsplit('/', 1)[-1] + '.html'
    path = os.path.join(folder, filename)
    log.debug(path)

    if os.path.exists(path):
        with open(path, 'r') as f:
            s = f.read()
            log.info(f'read the file {filename}')
            return s
    else:
        # create cached dir
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 发送网络请求, 把结果写入到文件夹中
        # request, and write the result to the dir
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        r = requests.get(url, headers=headers)
        with open(path, 'w') as f:
            log.info(f'write to {path}')
            f.write(r.content)
    return r.content


class Model(object):
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            log.debug(f'{k} {v}')
            self.__setattr__(k, v)


def movie_from_div(div):
    e = pq(div)

    m = Movie(
        title=e('.name').text(),
        actors=e('.star').text().split('：')[-1],
        release=e('.releasetime').text().split('：')[-1],
        score=e('.score').text(),
    )
    return m


def movies_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.board-wrapper dd')
    movies = [movie_from_div(i) for i in items]
    return movies


def get_movies():
    link = 'https://maoyan.com/board'
    movies = movies_from_url(link)
    log.debug(movies)
    return movies
