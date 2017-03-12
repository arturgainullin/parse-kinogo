import requests
from bs4 import BeautifulSoup
import re
import sensitive_analysis



main_url="http://kinogo.club"
url_const="http://kinogo.club/page/"

def get_html(url):
        response = requests.get(url)
        response.encoding = 'windows-1251' #fix encoding, requests lib identifies it incorrectly for kinogo.club site
        soup = BeautifulSoup(response.text, 'lxml', from_encoding='windows-1251')
        return soup

class film:
    def __init__(self, shortstory):
        self.link = shortstory.find('h2', class_='zagolovki').a.get('href').strip()
        info_with_blank_lines = shortstory.find('div', class_='shortimg').get_text()
        lines = info_with_blank_lines.split('\n')
        info=""
        for line in lines:
            if not re.match(r'^\s*$', line):
                info = info + line
        try:
            self.description = re.match(r'(.*)Год выпуска.*', info).group(0);
        except:
            self.description = ""
        try:
            self.production_year = re.match(r'.*Год выпуска:\s*(.*)Страна.*', info).group(1);
        except:
            self.production_year = 0
        try:
            self.country = re.match(r'.*Страна:\s*(.*)Жанр.*', info).group(1);
        except:
            self.country = ""
        try:
            self.video = re.match(r'.*Качество:\s*(.*)Перевод.*', info).group(1);
        except:
            self.video = ""
        try:
            self.audio = re.match(r'.*Перевод:\s*(.*)Продолжительность.*', info).group(1);
        except:
            self.audio =""
        try:
            self.time = re.match(r'.*Продолжительность:\s*(.*)Премьера.*', info).group(1);
        except:
            self.time = ""

        soup = get_html(self.link)
        comment_elements = soup.find_all('div', class_='comentarii')
        self.comments = []
        for element in comment_elements:
            self.comments.append(element.get_text())
        self.like = 0
        self.dislike = 0
        self.rating = 0

    def statistics(self):
        try:
            features = sensitive_analysis.vectorizer.transform(self.comments)
            prediction = sensitive_analysis.lr.predict(features)
            for score in prediction:
                if score > 8:
                    self.like = self.like + 1
                else:
                    self.dislike = self.dislike + 1
            if not (self.like == 0 and self.dislike == 0):
                self.rating = int(self.like / (self.like + self.dislike) * 100)
        except:
            self.like = 0
            self.dislike = 0

    def __str__(self):
        return self.link + " Rating: " + str(self.rating)

def key_func(film):
    return film.rating

def main():
    soup = get_html(main_url)
    #get pages amount
    pages_num = soup.find('div', class_='bot-navigation').find_all('a')[-2].contents
    films = []
    for page in range(1, int(pages_num[0]) + 1):
        url = url_const + str(page)
        soup = get_html(url)
        shortstories = soup.find_all('div', class_='shortstory')
        for shortstory in shortstories:
            iter_film = film(shortstory)
            iter_film.statistics()
            films.append(iter_film)
            films.sort(key=key_func, reverse=True)
    #print 5 best movies
    for i in range(5):
        print(films[i])

if __name__ == '__main__':
    main()
