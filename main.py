from utils import *
import requests
from functools import reduce
from pyquery import PyQuery as pq

config = Dict(
    cache='./raw/xiaozhu/',
    based_url='http://bj.xiaozhu.com/search-duanzufang-p{}-0/',
    number=20,
    # There're 24 detail_link in per-page
    detail_link_selector='#page_list > ul > li:nth-child({}) > a',
)

detail_page_selector = Dict(
    title='div.pho_info > h4',
    # body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span
    address='span.pr5',
    price='#pricePart > div.day_l',
    landlorder='#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a'
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
        save_to_local(f'{config.cache}{path}/', i, u.text)


def read_raws(links, path):
    '''
    1. read the cache of pages, and if it's not exist, download it and save to the path!
    2. return the list of cached html, and parse it!.
    '''
    # todo p is coupling
    p = f'{config.cache}{path}/'
    ls = files(p)
    if len(ls) == 0:
        download_pages(links, path)
        ls = files(p)
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
        remove_dir(config.cache_path)
        download_pages(based_urls, 'based_page')

    # return all detail_link of one page
    def one_page_links(d):
        return (d(
            config.detail_link_selector.format(i + 1)).attr['href'] for i in range(0, 24))

    def filter_none(arr):
        return list(filter(lambda x: x is not None, arr))

    # FP make me happy
    detail_links = set(reduce(lambda acc, d: acc +
                              filter_none(one_page_links(d)), read_raws(based_urls, 'based_page'), []))

    def get_info(d):
        r = dict()
        for k, v in detail_page_selector.items():
            t = d(v).text()
            if t:
                # Chrome dev-tools selector dese not working in same case?
                r[k] = t
        return r

    res = list(map(get_info, read_raws(detail_links, 'detail_links')))

    save_jsonify(res, './result.json')


if __name__ == '__main__':
    main()
