import requests
import re
from time import sleep


def get_proxy_ip():
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    url = 'https://ip.ihuan.me/'
    page = '?page=645pdd5b9'
    get_paged = []
    re_connect = 5
    while re_connect > 0:
        try:
            resp = requests.get(url + page, headers=user_agent, timeout=10)
        except requests.exceptions.RequestException as e:
            print(e)
            re_connect -= 1
        else:
            re_connect = 5
            ip = re.findall('[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}', resp.text)
            port = re.findall('<td>[0-9]+</td>', resp.text)
            pages = re.findall('[?]page=[0-9a-z]{1,9}', resp.text)
            with open('proxyIp.txt', 'a') as f:
                for i, j in zip(ip, port):
                    f.write(i)
                    f.write('    ')
                    f.write(j[4:-5])
                    f.write('\n')
            if len(pages) == 0:
                break
            page = pages[-1]
            if page in get_paged:
                break
            get_paged.append(page)
            print(url + page + '\n')
        sleep(range(3, 10))


if __name__ == '__main__':
    get_proxy_ip()
