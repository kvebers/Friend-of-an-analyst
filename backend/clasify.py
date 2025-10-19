import joblib
import re, string
import pandas as pd

LR = joblib.load("classification_models/logistic_model.pkl")
DT = joblib.load("classification_models/decision_tree_model.pkl")
GB = joblib.load("classification_models/gradient_boost_model.pkl")
RF = joblib.load("classification_models/random_forest_model.pkl")
vektor = joblib.load("classification_models/tfidf_vectorizer.pkl")

def remove(text):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\\W', ' ', text)
    text = re.sub(r'https?://\S+|www.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

def output_label(n):
    if n == 0:
        return "Informācija ir aplama!"
    elif n == 1:
        return "Informācija ir patiesa!"
    else:
        return "ERROR"


def predict_label(news):
    print("I am here")
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test['text'].apply(remove)
    new_x_test = new_def_test['text']
    new_xv_test = vektor.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)[0]
    pred_DT = DT.predict(new_xv_test)[0]
    pred_GB = GB.predict(new_xv_test)[0]
    pred_RF = RF.predict(new_xv_test)[0]
    predictions = [pred_LR, pred_DT, pred_GB, pred_RF]
    majority = max(set(predictions), key=predictions.count)
    return output_label(majority)
