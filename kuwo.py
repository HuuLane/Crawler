import requests
from pyquery import PyQuery as pq


def main():
    link = 'https://www.kugou.com/yy/rank/home/1-8888.html?from=rank'
    d = pq(requests.get(link).text)
    selector = '#rankWrap > div.pc_temp_songlist > ul > li:nth-child({}) > a'

    def get_info(i):
        t = d(selector.format(i)).text()
        return dict(
            rank=i,
            title=t,
        )

    data = list(map(get_info, range(1, 22+1)))


if __name__ == "__main__":
    main()
