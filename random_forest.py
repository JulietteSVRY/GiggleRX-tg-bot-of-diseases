import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from collections import OrderedDict
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
def StartModel():
    training = pd.read_csv('Data/Training.csv')
    #print(training.columns[:-1])
    cols = training.columns
    cols = cols[:-1]
    x = training[cols]
    In = training[cols].iloc[0]
    # print(In)
    for i in range(len(In)):
        In.iloc[i] = 0
    y = training['prognosis']
    y1 = y

    reduced_data = training.groupby(training['prognosis']).max()
    #mapping strings to numbers
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = le.transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    # creating RF classifier
    clf = RandomForestClassifier(n_estimators=100)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.40)
    # Training the model on the training dataset
    # fit function is used to train the model using the training sets as parameters
    clf.fit(X_train.values, y_train)

    # performing predictions on the test dataset
    y_pred = clf.predict(X_test)

    # metrics are used to find accuracy or error
    from sklearn import metrics
    print()

    # using metrics module for accuracy calculation
    print("ACCURACY OF THE MODEL: ", metrics.accuracy_score(y_test, y_pred))
    return clf, le


#enter first symptom:
def SimiliarSymptoms(first_symptom):
    training = pd.read_csv('Data/Training.csv')

    #print(training.columns[:-1])
    cols = training.columns

    cols = cols[:-1]
    x = training[cols]
    select = x.loc[x[first_symptom] == 1]
    sums1 = dict(select.sum())
    sums = OrderedDict(sorted(sums1.items()))
    first_score = sums.pop(first_symptom)
    # print(select.sum())
    score = {}
    for i in sums:

        s = sums[i] * (1 / first_score)
        # print(s)
        if s >= 0.35:
            score[i] = 1 - s

    score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1])}
    # selectUniq = training.loc[training[first_symptom] == 1]['prognosis'].unique()

    symptoms = [first_symptom]

    for i in score:
        if len(symptoms) == 4:
            break
        else:
            symptoms.append(i)
    return symptoms


def GetDisease(symptoms):
    training = pd.read_csv('Data/Training.csv')
    cols = training.columns[:-1]
    clf, le = StartModel()
    print('Model trained')
    In = training[cols].iloc[0]
    for i in symptoms:
        In[i] = 1
    print('Predicting now')
    print(np.array(In))
    condition = clf.predict(np.array(In).reshape(1, -1))
    # print(condition)
    print(condition)
    disease = le.inverse_transform(condition)[0]
    return (disease)


def DiseaseInfo(disease, symptoms, days):
    severity = pd.read_csv('Data/Symptom_severity.csv')
    precaution = pd.read_csv('Data/Symptom_precaution.csv')
    desc = pd.read_csv('Data/Symptom_Description.csv')
    #CALCULATE SEVERITY
    sever = 0
    for i in symptoms:
        sever += int(severity[i])
    # print(sever)
    sever *= days
    sever *= 1 / len(list(symptoms))
    # print(sever)
    if (sever > 13):
        sever_out = "You should take the consultation from doctor. "
    else:
        sever_out = "It might not be that bad but you should take precautions."
    desc_out = desc[disease].iloc[0]
    pre = precaution.loc[precaution['Disease'] == disease]
    print('The precautions to follow are: ')
    print('1: ', pre.iloc[0][1])
    print('2: ', pre.iloc[0][2])
    print('3: ', pre.iloc[0][3])
    return sever_out, desc_out, [pre.iloc[0][1], pre.iloc[0][2], pre.iloc[0][3]]
