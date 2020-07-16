import requests
import re
from time import sleep
import random


def get_from_ihuan(store_file_path):
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    url = 'https://ip.ihuan.me/'
    page = '?page=1'
    get_paged = ['?page=1']
    re_connect = 5
    line_num = 0
    while re_connect > 0:
        try:
            resp = requests.get(url + page, headers=user_agent, timeout=10)
        except requests.exceptions.RequestException as e:
            print(e)
            re_connect -= 1
        else:
            ip = re.findall('[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}', resp.text)
            port = re.findall('<td>[0-9]+</td>', resp.text)
            if len(ip) == 0 or len(port) == 0:
                re_connect -= 1
                continue
            pages = re.findall('[?]page=[0-9a-z]+', resp.text)
            find_page = False
            for p in pages[2:]:
                if p not in get_paged:
                    page = p
                    find_page = True
                    get_paged.append(page)
                    break
            if not find_page:
                re_connect -= 1
                continue
            with open(store_file_path, 'a') as f:
                for i, j in zip(ip, port):
                    f.write(i)
                    f.write(':')
                    f.write(j[4:-5])
                    f.write('\n')
            re_connect = 5
            line_num += 1
            print(str(line_num) + ' : ' + url + page + '\n')
        sleep(random.randint(3, 10))


if __name__ == '__main__':
    get_from_ihuan('proxyIp.txt')
