import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression

#Read train data
file = open('train_data_scored.csv', 'r')
raw_data = pandas.read_csv(file)

#Fit model and get features sparse matrix for train data
#We will use this sparse matrix to fit linear regressio model
vectorizer = TfidfVectorizer()
train_feature_matrix = vectorizer.fit_transform(raw_data['Comment'])

#Fit linear regression model using sparse data
lr = LinearRegression()
lr.fit(train_feature_matrix, raw_data['Score'])
#print(lr.score(train_feature_matrix, raw_data['Score']))
