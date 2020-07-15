import requests
import toml
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Doujinshi(Base):
    __tablename__ = 'Doujinshi_collections'
    id = Column(Integer, primary_key=True)

    title_gn = Column(String)
    title_gj = Column(String)
    url = Column(String)
    rating_count = Column(Integer)
    rating_score = Column(REAL)

    def __init__(self, title_gn, title_gj, url, rating_count, rating_score) -> None:
        self.title_gn = title_gn
        self.title_gj = title_gj
        self.url = url
        self.rating_count = rating_count
        self.rating_score = rating_score


if __name__ == '__main__':
    EXAMPLE_LINK = 'https://exhentai.org/g/1684029/6b7760bb5c/'

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

                gn = soup.select_one('#gn').text
                gj = soup.select_one('#gj').text
                count = soup.select_one('#rating_count').text
                score = soup.select_one('#rating_label').text[9:]

                doujinshi = Doujinshi(gn, gj, link, count, score)
                print(gn)

                engine = create_engine('sqlite:///data.db')
                Base.metadata.create_all(engine)
                session = sessionmaker(bind=engine)()
                session.add(doujinshi)
                session.commit()

                print(doujinshi.title_gj)
