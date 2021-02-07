import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader
from sklearn import tree

clf = tree.DecisionTreeRegressor(max_depth=4)

prologSessions1920 = pd.read_csv("Project SlayTheDragon\Datafiles\PrologSessions1920.csv")

# Splits op zodat amount of submissions opgesplitst is per oefenzitting.

session01, session02, session03, session04, sessionindividual = [], [], [], [], []
score01, score02, score03, score04, scoreIndividual = [], [], [], [], []

# Per student zal er dus 1 element zijn: Het aantal submissions.
for x in range(int(len(prologSessions1920['user_id']) * 0.9)):
    if prologSessions1920['category'][x] == 8:
        session01.append([prologSessions1920['Submission_Amount'][x]])
        score01.append([prologSessions1920['score_prolog'][x]])
    elif prologSessions1920['category'][x] == 9:
        session02.append([prologSessions1920['Submission_Amount'][x]])
        score02.append([prologSessions1920['score_prolog'][x]])
    elif prologSessions1920['category'][x] == 10:
        session03.append([prologSessions1920['Submission_Amount'][x]])
        score03.append([prologSessions1920['score_prolog'][x]])
    elif prologSessions1920['category'][x] == 12:
        session04.append([prologSessions1920['Submission_Amount'][x]])
        score04.append([prologSessions1920['score_prolog'][x]])
    else:
        sessionindividual.append([prologSessions1920['Submission_Amount'][x]])
        scoreIndividual.append([prologSessions1920['score_prolog'][x]])

treeSession01 = clf.fit(session01, score01)
treeSession02 = clf.fit(session02, score02)
treeSession03 = clf.fit(session03, score03)
treeSession04 = clf.fit(session04, score04)
# treeSessionIndividual = clf.fit(sessionindividual,scoreIndividual)


# Building the BIG Tree

# Nu hebben we de bomen, nu willen we zorgen dat we effectief iets kunnen voorspellen?

correct = 0
incorrect = 0

for x in range(int(len(prologSessions1920['user_id']) * 0.9), len(prologSessions1920['user_id'])):
    if prologSessions1920['category'][x] == 8:
        pred = treeSession01.predict(prologSessions1920['Submission_Amount'][x])
    elif prologSessions1920['category'][x] == 9:
        pred = treeSession02.predict(prologSessions1920['Submission_Amount'][x])
    elif prologSessions1920['category'][x] == 10:
        pred = treeSession03.predict(prologSessions1920['Submission_Amount'][x])
    elif prologSessions1920['category'][x] == 12:
        pred = treeSession04.predict(prologSessions1920['Submission_Amount'][x])
    else:
        pred = treeSessionIndividual.predict([prologSessions1920['Submission_Amount'][x]])[0]

    score = prologSessions1920['score_prolog'][x]
    print(pred, score)
    if ((pred <= 5 and score > 5) or (pred > 5 and score <= 5)):
        incorrect += 1
    else:
        correct += 1
print(correct, incorrect)
