import joblib
import re, string
import pandas as pd


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
    LR = joblib.load("classification_models/logistic_model.pkl")
    DT = joblib.load("classification_models/decision_tree_model.pkl")
    GB = joblib.load("classification_models/gradient_boost_model.pkl")
    RF = joblib.load("classification_models/random_forest_model.pkl")
    vektor = joblib.load("classification_models/tfidf_vectorizer.pkl")
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test['text'].apply(remove)
    new_x_test = new_def_test['text']
    print("I was here")
    print(new_x_test)
    new_xv_test = vektor.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)[0]
    pred_DT = DT.predict(new_xv_test)[0]
    pred_GB = GB.predict(new_xv_test)[0]
    pred_RF = RF.predict(new_xv_test)[0]
    probs = [
        LR.predict_proba(new_xv_test)[0][1],
        DT.predict_proba(new_xv_test)[0][1],
        GB.predict_proba(new_xv_test)[0][1],
        RF.predict_proba(new_xv_test)[0][1]
    ]
    #total_prob = sum(probs)  
    print(probs)
    print(pred_LR)
    print(pred_DT)
    print(pred_GB)
    print(pred_RF)
    majority = 0
    if (pred_DT or pred_GB or pred_RF or pred_LR):
        majority = 1

    return output_label(majority)


if __name__ == "__main__":
    text = '''As U.S. budget fight looms, Republicans flip their fiscal script","WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress, who voted this month for a huge expansion of the national debt to pay for tax cuts, called himself a “fiscal conservative” on Sunday and urged budget restraint in 2018. In keeping with a sharp pivot under way among Republicans, U.S. Representative Mark Meadows, speaking on CBS’ “Face the Nation,” drew a hard line on federal spending, which lawmakers are bracing to do battle over in January. When they return from the holidays on Wednesday, lawmakers will begin trying to pass a federal budget in a fight likely to be linked to other issues, such as immigration policy, even as the November congressional election campaigns approach in which Republicans will seek to keep control of Congress. President Donald Trump and his Republicans want a big budget increase in military spending, while Democrats also want proportional increases for non-defense “discretionary” spending on programs that support education, scientific research, infrastructure, public health and environmental protection. “The (Trump) administration has already been willing to say: ‘We’re going to increase non-defense discretionary spending ... by about 7 percent,’” Meadows, chairman of the small but influential House Freedom Caucus, said on the program. “Now, Democrats are saying that’s not enough, we need to give the government a pay raise of 10 to 11 percent. For a fiscal conservative, I don’t see where the rationale is. ... Eventually you run out of other people’s money,” he said. Meadows was among Republicans who voted in late December for their party’s debt-financed tax overhaul, which is expected to balloon the federal budget deficit and add about $1.5 trillion over 10 years to the $20 trillion national debt. “It’s interesting to hear Mark talk about fiscal responsibility,” Democratic U.S. Representative Joseph Crowley said on CBS. Crowley said the Republican tax bill would require the  United States to borrow $1.5 trillion, to be paid off by future generations, to finance tax cuts for corporations and the rich. “This is one of the least ... fiscally responsible bills we’ve ever seen passed in the history of the House of Representatives. I think we’re going to be paying for this for many, many years to come,” Crowley said. Republicans insist the tax package, the biggest U.S. tax overhaul in more than 30 years,  will boost the economy and job growth.'''
    predict_label(text)