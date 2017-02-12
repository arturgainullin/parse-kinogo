import pandas
from sklearn.feature_extraction.text import TfidfVectorizer


file = open('train_data_scored.csv', 'r')
csv = pandas.read_csv(file)

print(csv.head())
