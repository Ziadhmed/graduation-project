import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('stopwords')
stopwords=nltk.corpus.stopwords.words('english')
#Load the csv file
phishing_dataset = pd.read_csv("emails.csv")
# Select Dependent and Independent Variables
x=phishing_dataset["text"]
y=phishing_dataset["spam"]
#x has text so it must be preprocessed first before splitting and training
x_remove_link=[re.sub(r"http\S+","",text) for text in x]
x_remove_char=[re.sub("[^a-zA-Z0-9]"," ",text) for text in x_remove_link]
x_lower=[text.lower() for text in x_remove_char]
x_token=[nltk.word_tokenize(text) for text in x_lower]
x_prepared=[[word for word in text if word not in stopwords] for text in x_token]
cv=CountVectorizer(max_features=2000)
x=cv.fit_transform(" ".join(text) for text in x_prepared).toarray()

#split the data set into train and test
x_train,x_test,y_train,y_test=train_test_split(x, y,test_size=0.3,random_state=42)

#instantiate the model
clf=RandomForestClassifier(n_estimators = 100, random_state = 42)

#training sthe model
clf.fit(x_train,y_train)

#make pickle file of our model
pickle.dump(clf, open("model.pkl","wb"))


