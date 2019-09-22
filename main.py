from utils import *
import requests
from functools import reduce
from pyquery import PyQuery as pq

config = Dict(
    cache_path='./raw/xiaozhu/',
    # There're 24 detail_link in per-page
    detail_link='#page_list > ul > li:nth-child({}) > a',
)


def save_to_local(i: int, text: str) -> None:
    c = i + 1
    index = f'{c}' if c > 9 else f'0{c}'
    write_file(f'{config.cache_path}{index}.html', text)


def download_pages(count: int) -> None:
    # client info
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    base_url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'

    for i in range(0, count):
        # the downloaded filenames 00, 01... 10, 11...
        u = requests.get(base_url.format(i), headers=headers)
        save_to_local(i, u.text)


def read_raws():
    '''
    1. read the cache of pages, and if it's not exist, download it and save!
    2. return the list of cached html, and parse it!.
    '''
    ls = files(config.cache_path)
    if len(ls) == 0:
        download_pages(20)
        ls = files(config.cache_path)
    for f_name in ls:
        log('Read the file: ', f_name)
        yield pq(filename=f_name)


def main():
    import sys

    # update
    if 'update' in sys.argv:
        # clear & download
        remove_dir(config.cache_path)
        download_pages(20)

    # return all detail_link of one page
    def one_page_links(d):
        return (d(
            config.detail_link.format(i + 1)).attr['href'] for i in range(0, 24))

    def filter_none(arr):
        return list(filter(lambda x: x is not None, arr))

    # FP make me happy
    detail_links = set(reduce(lambda acc, d: acc +
                              filter_none(one_page_links(d)), read_raws(), []))


if __name__ == '__main__':
    main()
