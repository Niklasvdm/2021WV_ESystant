import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt

clf = tree.DecisionTreeRegressor()
threshold_submissions = 0
threshold_completed = 0
csv1617 = pd.read_csv('/Users/informatica/Desktop/BP/1617UserIDNoSubNoComplscPPRscHKsc.csv')
csv1718 = pd.read_csv('/Users/informatica/Desktop/BP/1718UserIDNoSubNoComplscPPRscHKsc.csv')
csv1819 = pd.read_csv('/Users/informatica/Desktop/BP/1819UserIDNoSubNoComplscPPRscHKsc.csv')
csv1920 = pd.read_csv('/Users/informatica/Desktop/BP/1920UserIDNoSubNoComplscPPRscHKsc.csv')
indicators1617, score1617 = [], []
indicators1718, score1718 = [], []
indicators1819, score1819 = [], []
indicators1920, score1920 = [], []

for x in range(int(len(csv1617['user_id'])*0.9)):
    if (csv1617['nb_submissions'][x] >= threshold_submissions and csv1617['nb_completed'][x] >= threshold_completed):
        indicators1617.append([csv1617['nb_submissions'][x], csv1617['nb_completed'][x]])
        score1617.append(csv1617['score'][x])

for x in range(int(len(csv1718['user_id'])*0.9)):
    if (csv1718['nb_submissions'][x] >= threshold_submissions and csv1718['nb_completed'][x] >= threshold_completed):
        indicators1718.append([csv1718['nb_submissions'][x], csv1718['nb_completed'][x]])
        score1718.append(csv1718['score'][x])

for x in range(int(len(csv1819['user_id'])*0.9)):
    if (csv1819['nb_submissions'][x] >= threshold_submissions and csv1819['nb_completed'][x] >= threshold_completed):
        indicators1819.append([csv1819['nb_submissions'][x], csv1819['nb_completed'][x]])
        score1819.append(csv1819['score'][x])

for x in range(int(len(csv1920['user_id'])*0.9)):
    if (csv1920['nb_submissions'][x] >= threshold_submissions and csv1920['nb_completed'][x] >= threshold_completed):
        indicators1920.append([csv1920['nb_submissions'][x], csv1920['nb_completed'][x]])
        score1920.append(csv1920['score'][x])

indicators_to_predict= []
score_to_predict = []
for x in range(int(len(csv1617['user_id'])*0.9), len(csv1617['user_id'])):
    if (csv1617['nb_submissions'][x] >= threshold_submissions and csv1617['nb_completed'][x] >= threshold_completed):
        indicators_to_predict.append([csv1617['nb_submissions'][x], csv1617['nb_completed'][x]])
        score_to_predict.append(csv1718['score'][x])
for x in range(int(len(csv1718['user_id'])*0.9), len(csv1718['user_id'])):
    if (csv1718['nb_submissions'][x] >= threshold_submissions and csv1718['nb_completed'][x] >= threshold_completed):
        indicators_to_predict.append([csv1718['nb_submissions'][x], csv1718['nb_completed'][x]])
        score_to_predict.append(csv1718['score'][x])
for x in range(int(len(csv1819['user_id'])*0.9), len(csv1819['user_id'])):
    if (csv1819['nb_submissions'][x] >= threshold_submissions and csv1819['nb_completed'][x] >= threshold_completed):
        indicators_to_predict.append([csv1819['nb_submissions'][x], csv1819['nb_completed'][x]])
        score_to_predict.append(csv1819['score'][x])
for x in range(int(len(csv1920['user_id'])*0.9), len(csv1920['user_id'])):
    if (csv1920['nb_submissions'][x] >= threshold_submissions and csv1920['nb_completed'][x] >= threshold_completed):
        indicators_to_predict.append([csv1920['nb_submissions'][x], csv1920['nb_completed'][x]])
        score_to_predict.append(csv1920['score'][x])


clf1617 = clf.fit(indicators1617, score1617)
clf1718 = clf.fit(indicators1718, score1718)
clf1819 = clf.fit(indicators1819, score1819)
clf1920 = clf.fit(indicators1920, score1920)

indicators_all = indicators1617+indicators1718+indicators1819+indicators1920
score_all = score1617+score1718+score1819+score1920
clf_all = clf.fit(indicators_all, score_all)

plt.figure(figsize=(15,10))
tree.plot_tree(clf1617,filled=True)


def predict(csv, clf, year):
    correct = 0
    dev_correct = 0
    wrong = 0
    dev_wrong = 0
    for x in range(int(len(csv['user_id'])*0.9), len(csv['user_id'])):
        if(csv['nb_submissions'][x]>=threshold_submissions and csv['nb_completed'][x]>=threshold_completed):
            pred = clf.predict([[csv['nb_submissions'][x], csv['nb_completed'][x]]])[0]
            scr = csv['score'][x]
            if ((pred < 0.5 and scr<0.5 )or (pred >= 0.5 and scr>=0.5 )):
                correct+=1
                dev_correct += abs(pred-scr)
                #print("Correct, dev = " + str(abs(pred-scr)))
            else:
                wrong+=1
                dev_wrong += abs(pred - scr)
                #print("Wrong, dev = " + str(abs(pred-scr)))
    print("TOTAL for year {} is {}% correct: {} with dev = {}, {}% wrong: {} with dev = {}.".format(year,round(correct/(correct+wrong)*100),
                                                                                                    correct,
                                                                                        round(dev_correct / correct,4),
                                                                                        round((wrong/(correct+wrong))*100),wrong,
                                                                                        round(dev_wrong / wrong,4)))
   # tree.plot_tree(clf)

predict(csv1617,clf1617,"16-17")
predict(csv1718,clf1718,"17-18")
predict(csv1819,clf1819,"18-19")
predict(csv1920,clf1920,"19-20")

correct = 0
dev_correct = 0
wrong = 0
dev_wrong = 0
for x in range(len(score_to_predict)):
    pred = clf.predict([indicators_to_predict[x]])[0]
    print([indicators_to_predict[x]])
    print(clf.predict([indicators_to_predict[x]]))
    scr = score_to_predict[x]
    if ((pred < 0.5 and scr < 0.5) or (pred >= 0.5 and scr >= 0.5)):
        correct += 1
        dev_correct += abs(pred - scr)
        # print("Correct, dev = " + str(abs(pred-scr)))
    else:
        wrong += 1
        dev_wrong += abs(pred - scr)
        # print("Wrong, dev = " + str(abs(pred-scr)))
print("TOTAL for year {} is {}% correct: {} with dev = {}, {}% wrong: {} with dev = {}.".format("ALL",
                                                                                    round(correct/(correct+wrong)*100),
                                                                                    correct,
                                                                                    round(dev_correct / correct,4),
                                                                                    round((wrong/(correct+wrong))*100),
                                                                                    wrong,
                                                                                    round(dev_wrong / wrong,4)))

