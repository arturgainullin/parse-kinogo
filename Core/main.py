import requests
from bs4 import BeautifulSoup
import re

main_url="http://kinogo.club"
url_const="http://kinogo.club/page/"

class film:
    def __init__(self, shortstory):
        self.link = shortstory.find('h2', class_='zagolovki').a.get('href').strip()
        info = shortstory.find('div', class_='shortimg').get_text()
        self.description = re.match(r'(.*)Год выпуска.*', info).group(1);
        self.production_year = re.match(r'.*Год выпуска:\s*(.*)Страна.*', info).group(1);
        self.country = re.match(r'.*Страна:\s*(.*)Жанр.*', info).group(1);
        self.video = re.match(r'.*Качество:\s*(.*)Перевод.*', info).group(1);
        self.audio = re.match(r'.*Перевод:\s*(.*)Продолжительность.*', info).group(1);
        self.time = re.match(r'.*Продолжительность:\s*(.*)Премьера.*', info).group(1);

    def statistics(self):
        pass


def main():
    response = requests.get(main_url)
    response.encoding = 'windows-1251' #fix encoding, requests lib identifies it incorrectly
    soup = BeautifulSoup(response.text, 'lxml', from_encoding='windows-1251') #BeautifulSoup will transform text to Unicode
    #get pages amount
    pages_num = soup.find('div', class_='bot-navigation').find_all('a')[-2].contents

    for page in range(1, 4):#pages_num + 1):
        url = url_const + str(page)
        response = requests.get(url)
        response.encoding = 'windows-1251' #fix encoding, requests lib identifies it incorrectly
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='windows-1251') #BeautifulSoup will transform text to Unicode
        shortstory = soup.find('div', class_='shortstory')
        iter_film = film(shortstory)


if __name__ == '__main__':
    main()
