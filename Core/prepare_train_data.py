import csv
import main


def create_train_data():
    with open('train_sample.txt', 'w') as file:
        for page in range(1, 2):
            url = main.url_const + str(page)
            soup = main.get_html(url)
            shortstories = soup.find_all('div', class_='shortstory')
            for shortstory in shortstories:
                film_obj = main.film(shortstory)
                soup = main.get_html(film_obj.link)
                comments = soup.find_all('div', class_='comentarii')
                for comment in comments:
                    file.write(comment.text + '\n')
    file.close()




if __name__ == '__main__':
    create_train_data()
