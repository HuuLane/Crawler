from utils import *
import requests
from functools import reduce
from pyquery import PyQuery as pq
from math import ceil

config = Dict(
    cache='./raw/kuwo/',
    number=ceil(500 / 22),
    based_url='https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank',
    # There're 22 song's rank info in each page.
    per_num=22,
    selector='#rankWrap > div.pc_temp_songlist > ul > li:nth-child({}) > a',
)


def save_to_local(path, i: int, text: str) -> None:
    c = i + 1
    index = f'{c}' if c > 9 else f'0{c}'
    write_file(f'{path}{index}.html', text)


def download_pages(links, path) -> None:
    # client info
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }

    for i, l in enumerate(links):
        # the downloaded filenames is 00, 01... 10, 11...
        u = requests.get(l, headers=headers)
        save_to_local(f'{path}/', i, u.text)


def read_raws(links, path):
    '''
    1. read the cache of pages, and if it's not exist, download it and save to the path!
    2. return the list of cached html, and parse it!.
    '''
    # todo p is coupling
    ls = files(path)
    if len(ls) == 0:
        download_pages(links, path)
        ls = files(path)
    for f_name in ls:
        log('Read the file: ', f_name)
        yield pq(filename=f_name)


def main():
    import sys

    based_urls = (config.based_url.format(i)
                  for i in range(1, config.number+1))

    # update
    if 'update' in sys.argv:
        # clear & download
        remove_dir(config.cache)
        download_pages(based_urls, config.cache)

    def selector():
        return (config.selector.format(i) for i in range(1, config.per_num))

    def get_info(acc, d):
        return acc + [d(s).text() for s in selector()]

    res = list(reduce(get_info, read_raws(based_urls, config.cache), []))

    save_jsonify(res, './top500.json')


if __name__ == '__main__':
    main()
