import requests
import toml
from bs4 import BeautifulSoup

if __name__ == '__main__':
    with open('config.toml', 'r') as config_file:
        config_toml = toml.loads(config_file.read())
        config_file.close()

        proxies = {
            'http': '127.0.0.1:8118',
            'https': '127.0.0.1:8118',
        }

        with open('data.txt', 'r') as link_list_file:
            for link in link_list_file.readlines():
                link = link.replace('\n', '')

                session = requests.Session()
                session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/84.0.4147.89 Safari/537.36'})

                r = session.get(link, proxies=proxies, cookies=config_toml)
                soup = BeautifulSoup(r.text, 'html.parser')
                img_link_cover = soup.select_one('#gdt a')['href']

                r = session.get(img_link_cover, proxies=proxies, cookies=config_toml)
                soup = BeautifulSoup(r.text, 'html.parser')
                img_link = soup.select_one('#img')['src']

                link_split = link.split('/')
                file_name = link_split[-3] + '_' + link_split[-2] + '.' + str(img_link).split('.')[-1]

                with open('cover/' + file_name, 'wb') as img_file:
                    r = session.get(img_link, proxies=proxies, cookies=config_toml)
                    img_file.write(r.content)
                    img_file.close()

                    print(file_name)
