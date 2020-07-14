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

        for index in range(54):
            print('page' + str(index) + '... ')

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.116 Safari/537.36'})

            r = session.get('https://exhentai.org/?page=' + str(index) + '&f_search=uploader:BlossomPlus',
                            proxies=proxies, cookies=config_toml)
            soup = BeautifulSoup(r.text, 'html.parser')

            for tag in soup.findAll('a', href=True):
                if str(tag).__contains__('https://exhentai.org/g/') and str(tag).__contains__('[Chinese]'):
                    with open('data.txt', 'a') as file:
                        link = tag['href']
                        print(link)

                        file.write(link + '\n')
                        file.close()
