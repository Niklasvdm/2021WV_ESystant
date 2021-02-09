import TreeConstructor
import Queries
import Database_Functions
from sklearn import tree


host,root,passw = Database_Functions.NiklasConnectivity()
#host, root, passw = Database_Functions.MaxConnectivity()


my_tree_query = Queries.getQuery03()
database = "esystant1920"
#queryResult = Database_Functions.query_database_dataframe(host,root,passw,database,my_tree_query)
queryResult = Database_Functions.get_query_database(host,root,passw,database,my_tree_query)
#print(queryResult)

(datapoints,grades, categories,categoriesAndLanguages) = Database_Functions.groupByUserGradesAndCategories(queryResult)

#for x in datapoints:
#    print(x + ': ' + str(len(datapoints[x])))
#    print(datapoints[x][0])
(testDict,verificationDict) = TreeConstructor.splitBase(datapoints)

(categoryUsers,categoryGrades,splitCategories)  = TreeConstructor.prepareCategories(testDict,grades,categories,categoriesAndLanguages)


myDecisionTrees = TreeConstructor.buildTrees(categoryUsers,categoryGrades)

#Okay, we've got a dictionary with { KEY : VALUE } ,
#       KEY == CATEGORY
#       VALUE == DECISION TREE


(megatreepredictions,megatreescores) = TreeConstructor.make_predictionswithgrades(testDict,grades,myDecisionTrees,categories)
#for i in range(len(megatreescores)):
#    print(megatreepredictions[i] , megatreescores[i])

clf = tree.DecisionTreeRegressor(max_depth = 3)
myMegaTree = clf.fit(megatreepredictions,megatreescores)

(predictedVerification,actualVerification) = TreeConstructor.make_predictionswithgrades(testDict,grades,myDecisionTrees,categories)
predictedScores = myMegaTree.predict(predictedVerification)


#   TODO:       HEEFT DE PLAATSING DE NULLEN EFFECT OP EINDRESULTAAT
# [0 for _ in range(len(list)]
#  Category = c

#
#       INPUT: [[SCORE_PROLOG_0,SCORE_HASKELL_0],...]
#               [[SCORE_PROLOG_0,SCORE_HASKELL_0],...]
#
#
def passFail(prediction,actual):
    correctscores = []
    for i in range(len(prediction)):
        result = [True,True]
        resultboth = True
        if ( ((prediction[i][0] > 5) and (actual[i][0] > 5) ) or ( (prediction[i][0] <= 5) and (actual[i][0] <= 5) ) ):
            result[0] = result[0] and True
        else:
            result[0] = result[0] and False
        if ( ((prediction[i][1] > 5) and (actual[i][1] > 5) ) or ( (prediction[i][1] <= 5) and (actual[i][1] <= 0) ) ):
            result[1] = result[1] and True
        else:
            result[1] = result[1] and False
        if((prediction[i][0] + prediction[i][1] < 10) and (actual[i][0]+actual[i][1] > 10)
        or ((prediction[i][0] + prediction[i][1] > 10) and (actual[i][0]+actual[i][1] < 10))):
            resultboth = False
        correctscores.append([result,resultboth])

    return correctscores
predictedList = predictedScores.tolist()
print(passFail(predictedList,actualVerification))

def averageDeviation(prediction,actual):
    return sum([prediction[x][y]-actual[x][y] for x in range(len(prediction)) for y in range(len(prediction[0]))])/(2*len(prediction))


print(averageDeviation(predictedList,actualVerification))
