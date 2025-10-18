import pandas as pd
import numpy as nump #bibliotēka izmantota mašīn mācībā
import seaborn as sb #datu vizualizācija
from sklearn.model_selection import train_test_split #dala masīvus nejaušās apakškopās priekš mācīšanās un testa datiem
import matplotlib.pyplot as plt #Ļaus attēlot grafiski datus
from sklearn.metrics import accuracy_score #Aprēķina patiesuma punktus
from sklearn.metrics import classification_report #Četri rādītāji TP(True Positive); TN(True negative); FP; FN
import re
import string

fake_data = pd.read_csv(r'C:/Users/37127/Desktop/Friend for an analyst/Fake.csv') #atver failu ar aplamo informāciju (lai mācītos izmanto)
true_data = pd.read_csv(r'C:/Users/37127/Desktop/Friend for an analyst/True.csv') #atver failu ar patieso informāciju

fake_data['class'] = 0
true_data['class'] = 1

#Sadalam datus priekš manuālās testēšanas
fake_mtest = fake_data.tail(10)
for i in range(23471, 23481, -1):
    fake_data.drop([i], axis = 0, inplace = True) #Nometam testa datus no kopējiem
true_mtest = true_data.tail(10)
for i in range(21407, 21417, -1):
    true_data.drop([i], axis = 0, inplace = True)


fake_mtest['class'] = 0
true_mtest['class'] = 1

mtest= pd.concat([true_mtest,fake_mtest],axis=0) #saglabā datus, lai varētu izmantot tālāk
mtest.to_csv("mtest.csv")

#Datu savienošana

SavienotiDati = pd.concat([true_data,fake_data],axis=0) 

nepieciesamie = SavienotiDati.drop(["title","subject","date"],axis=1) #Nometam nevajadzīgās kolonas ar info
nepieciesamie = nepieciesamie.sample(frac=1) #Sajaucam kārtību

def remove(data): #Noņemam nevajadzīgās zīmes no lapas, lai spētu veikt pārbaudi
    data = data.lower()
    data = re.sub('\[.*?\]','',data)
    data = re.sub('\\W',' ',data)
    data = re.sub('https?://\S+|www.\S+','',data)
    data = re.sub('<.*?>+','',data)
    data = re.sub('[%s]'%re.escape(string.punctuation),'',data)
    data = re.sub('\n','',data)
    data = re.sub('\w*\d\w','',data)
    return data
nepieciesamie['text']= nepieciesamie['text'].apply(remove)
nepieciesamie.head()

#Pārveido zināmo burtu tekstu par numurētu
x = nepieciesamie['text'] #Izveidojam atkarīgo un neatkarīgo vērtību apreķinos
y = nepieciesamie['class']

