import pandas as pd
import nltk
import numpy as np #bibliotēka izmantota mašīn mācībā
import seaborn as sb #datu vizualizācija
from sklearn.model_selection import train_test_split #dala masīvus nejaušās apakškopās priekš mācīšanās un testa datiem
import matplotlib.pyplot as plt #Ļaus attēlot grafiski datus
from sklearn.metrics import accuracy_score #Aprēķina patiesuma punktus
from sklearn.metrics import classification_report #Četri rādītāji TP(True Positive); TN(True negative); FP; FN
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer #Vektoru skaitītājs
from sklearn.linear_model import LogisticRegression #Klasificētu problēmu risināšanā izmanto
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords

fake_data = pd.read_csv('Fake.csv') #atver failu ar aplamo informāciju (lai mācītos izmanto)
true_data = pd.read_csv('True.csv') #atver failu ar patieso informāciju

fake_data['class'] = 0
true_data['class'] = 1

#Sadalam datus priekš manuālās testēšanas
fake_mtest = fake_data.tail(10).copy()
fake_data.drop(fake_data.tail(10).index, axis = 0, inplace = True)
true_mtest = true_data.tail(10).copy()
true_data.drop(true_data.tail(10).index, axis = 0, inplace = True)

fake_mtest['class'] = 0
true_mtest['class'] = 1

#mtest= pd.concat([true_mtest,fake_mtest],axis=0) #saglabā datus, lai varētu izmantot tālāk, bet tomēr laikam nebūs nepieciešami
#mtest.to_csv("mtest.csv")

#Datu savienošana

SavienotiDati = pd.concat([true_data,fake_data],axis=0) 

nepieciesamie = SavienotiDati.drop(["title","subject","date"],axis=1) #Nometam nevajadzīgās kolonas ar info
nepieciesamie = nepieciesamie.sample(frac=1, random_state=42) #Sajaucam kārtību

nepieciesamie.reset_index(inplace=True)
nepieciesamie.drop(['index'], axis = 1, inplace=True)

def remove(text): #Noņemam nevajadzīgās zīmes no lapas, lai spētu veikt pārbaudi
    text = str(text).lower()
    text = re.sub(r'\[.*?\]','',text)
    text = re.sub(r'\\W',' ',text)
    text = re.sub(r'https?://\S+|www.\S+','',text)
    text = re.sub(r'<.*?>+','',text)
    text = re.sub(r'[%s]'%re.escape(string.punctuation),'',text)
    text = re.sub(r'\n','',text)
    text = re.sub(r'\w*\d\w*','',text)

    return text
nepieciesamie['text']= nepieciesamie['text'].apply(remove)

#Pārveido zināmo burtu tekstu par numurētu
x = nepieciesamie['text'] #Izveidojam atkarīgo un neatkarīgo vērtību apreķinos
y = nepieciesamie['class']
x_train, x_test, y_train,y_test=train_test_split(x,y,test_size=0.25, random_state=42)#atdala mācīšanās un treniņa datus

vektor = TfidfVectorizer(stop_words='english', max_df=0.7, ngram_range=(1, 2)) # max_df = 0.7 ignorēs vārdus, kas parādās vairāk nekā 70% dokumentu
xv_train = vektor.fit_transform(x_train) # x vektoru apmācība
xv_test = vektor.transform(x_test) # x vektoru tests

#Modeļa apmācība

def model_evaluation(model, name, xv_train, y_train, xv_test, y_test):
    model.fit(xv_train, y_train)
    predictions = model.predict(xv_test)
    score = model.score(xv_test, y_test)
    
    print(f"--- {name} ---")
    print(f"Precizitāte (Accuracy): {score:.4f}")
    print("Klasifikācijas pārskats:")
    print(classification_report(y_test, predictions))
    return model

LR = model_evaluation(LogisticRegression(random_state=42, class_weight = 'balanced'), "Logistic Regression", xv_train, y_train, xv_test, y_test)
DT = model_evaluation(DecisionTreeClassifier(random_state=42, class_weight='balanced', max_depth=8), "Decision Tree", xv_train, y_train, xv_test, y_test)
GB = model_evaluation(GradientBoostingClassifier(random_state=42), "Gradient Boosting", xv_train, y_train, xv_test, y_test)
RF = model_evaluation(RandomForestClassifier(random_state=42, class_weight='balanced', max_depth=12), "Random Forest", xv_train, y_train, xv_test, y_test)

#LR - Aprēķina varbūtību, ka ziņa pieder klasei 1 (patiesai)
#DT - Klasificē datus pēc jā/nē jautājumiem
#GB - Savāc visu "koku" balsis, lai izteiktu gala vērtējumu (izmanto asembleri)
#RF -

#Manuāla pārbaude:
def output_label(n):
    if n==0:
        return "Informācija ir aplama!"
    elif n==1:
        return "Informācija ir patiesa!"

    else:
        return "ERROR"
    
def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test['text'].apply(remove)
    new_x_test = new_def_test['text']
    new_xv_test = vektor.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GB = GB.predict(new_xv_test)
    pred_RF = RF.predict(new_xv_test)
    
    return print(f'''\n
                    LR Prediction: {output_label(pred_LR[0])}\n
                    DT Prediction: {output_label(pred_DT[0])}\n
                    GB Prediction: {output_label(pred_GB[0])}\n
                    RF Prediction: {output_label(pred_RF[0])}\n
                 ''')

news = str(input("Ievadiet informāciju: "))
manual_testing(news)

