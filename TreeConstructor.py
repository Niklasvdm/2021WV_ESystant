from random import shuffle

from sklearn import tree


######## FUNCTIONS:
#
#   ~ splitBase
#
#           INPUT: Dictionary
#           OUTPUT: (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
#

# First thing we're going to do is just writing a function to fetch data. We write two: One given just a query and a
# database,  one more detailed with host info

# https://stackoverflow.com/questions/12988351/split-a-dictionary-in-half
# INPUT: DICTIONARY
# OUTPUT: TUPLE (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
#       Function takes the dictionary and shuffles it randomly to produce shuffled result.
def splitBase(d):
    temp = (list(d.items()))
    shuffle(temp)
    return dict(temp[:int(len(d) * TEST_PERCENTAGE)]), dict(temp[int(len(d) * TEST_PERCENTAGE):])


TEST_PERCENTAGE = 0.9
VERIFICATION_PERCENTAGE = 1 - TEST_PERCENTAGE


##################################################
# Nu willen we gewoon een functie kunnen geven dat een query ( en de nodige informatie neemt als input) en het resultaat van de decision tree meegeeft.
#   Dit wordt eventueel gedaan met verschillende hulpfuncties.
#       Om dit te doen werken : 1e kolom user id, 2e kolom per oefenzitting , laatste 2 kolommen Prolog & Haskell Respectively.
###################################################


#
# input: dictionary van per user verschillende arrays met eigenschappen. Dit in een dictionary
# output: Per categorie een boom op de overblijvende eigenschapper per user.
# {USER:[[CATEGORY_0,_],[CATEGORY_1,_],...]}
# CATEGORY_0 X [PROPERTY_0,PROPERTY_1,...] -> DECISION TREE_0 , CATEGORY_1 X [PROPERTY_0,PROPERTY_1,...] -> DECISION TREE_0
#
#   For each category we want to build a tree. This is done with preparecategories and buildTrees
#
# NEXT: BUILD MEGATREE
#       INPUT:
#       OUTPUT:
#
#


# Function that per Category, makes a dictionary with all of the user necessairy and a list with the necessairy grades
#       REQUIREMENT: EERSTE PLAATS IN DICTIONARY USER IS CATEGORIE,LAATSTE PLAATS IS TAAL.
#                       GRADESDICTIONARY KOMT OVEREEN MET [PUNT_PROLOG,PUNT_HASKELL]
#       INPUT : { USER : [[CAT_0,...,LANGUAGE],[CAT_1,...,LANGUAGE],...]] , .... }
#               { USER : [GRADE_PROLOG,GRADE_HASKELL],... }
#       OUTPUT : { ( CATEGORY_0 : [ [PROPERTY_0,PROPERTY_1,....],[PROPERTY_0,PROPERTY_1,...] ] ) , ( ...) , ....}
#                { ( CATEGORY_0 : [ GRADE_0_0,GRADE_0_1,...] ) , ( CATEGORY_1 : [ GRADE_1_0,GRADE_1_1,...] ) , ... }
#
#
def prepareCategories(testDictionary, gradesDictionary, categories, categoriesAndLanguage):
    exercizeDictionary = {}
    for number in categories: exercizeDictionary[number] = []
    exercizeGradeDictionary = {}
    for number in categories:  exercizeGradeDictionary[number] = []
    category_sets = [set(), set()]  # TODO : pass documentatie aan
    for users in testDictionary:  # ELKE USER HEEFT [[CAT_0,OPLEIDING_ID_0...,LANGUAGE],[CAT_1,OPLEIDING_ID_0...,LANGUAGE],...]
        oplID = testDictionary[users][0][0]
        length_properties = len(testDictionary[users][0]) - 3
        userSet = set()
        for user_list in testDictionary[users]:
            language = user_list[-1] % 2  # 1 voor haskell, 0 voor Prolog.
            category_sets[int(language)].add(user_list[0])
            exercizeDictionary[user_list[0]].append(user_list[1:-1])
            userSet.add(user_list[0])
        remaining_categories = categories - userSet
        for i in remaining_categories:
            templist = [oplID] + [0 for _ in range(length_properties)]
            exercizeDictionary[i].append(templist)
        for [catergory, language] in categoriesAndLanguage:
            exercizeGradeDictionary[catergory].append(gradesDictionary[users][int(language % 2)])
    # print(exercizeDictionary)

    return (exercizeDictionary, exercizeGradeDictionary, category_sets)


#            else:
#                exercizeDictionary[user_list[0]] = [user_list[1:-1]] #Neem eerst alle nuttige informatie.
#                gradeStudent = gradesDictionary[users][language] # Neem de grade van de student.
#                exercizeGradeDictionary[user_list[0]] = [gradeStudent] #Stop die in de lijst.


# DOEL VAN BUILDTREES: we bouwen een boom per categorie met de nodige punten
#   INPUT: { CATEGORY_0 : [ LIST_0_0 , LIST_0_1 , ... LIST_0,N0] , CATEGORY_1 : [ LIST_1_0 , LIST_1_1 , ... LIST_1,N1]  , .... }
#          { CATEGORY_0 : [ GRADE_0_0 , GRADE_0_1 , ... GRADE_0,N0] , CATEGORY_1 : [ GRADE_1_0 , GRADE_1_1 , ... GRADE_1,N1]  , .... }
#   OUTPUT: { CATEGORY_0 : DECISION_TREE_0  , CATEGORY_1 : DECISION_TREE_1  , ... }
def buildTrees(DictionaryCategories, DictionaryGrades):
    decisionTrees = {}
    # for number in categories : decisionTrees[number] = None
    for category in DictionaryCategories.keys():
        clf = tree.DecisionTreeRegressor(max_depth=3)
        listValues = DictionaryCategories[category]
        listGrades = DictionaryGrades[category]

        # print (len(listValues))
        # print(len(listGrades))
        decisionTrees[category] = clf.fit(listValues, listGrades)
    return decisionTrees


# TODO comments
def build_trees_with_dataframe(dataframe_to_train):
    decisionTrees = {}
    for category in dataframe_to_train['category'].unique():
        clf = tree.DecisionTreeRegressor(max_depth=3)
        data_cat = dataframe_to_train.loc[dataframe_to_train['category'] == category].drop(['user_id', 'category'],
                                                                                           axis=1)
        language = int(data_cat.iloc[0]['language'] % 2)  # 1 voor haskell, 0 voor Prolog.

        listValues = data_cat.drop(['language', 'score_prolog', 'score_haskell'], axis=1).values.tolist()
        listGrades = [x[language] for x in data_cat[['score_prolog', 'score_haskell']].values.tolist()]

        decisionTrees[category] = clf.fit(listValues, listGrades)
    return decisionTrees


# Purpose of next function -> Make a prediction with the testDict
# input: Dictionary of users and properties , Dictionary of users and their scores , Dictionary with categories and trees, possible categories.
#   { USER : [CATEGORY_ID, OPL_ID, ... , LANGUAGE] }
#
#
# OUTPUT:
#    [[PRED_0_0,PRED_0_1,....PRED_0_N],[PRED_1_0,PRED_1_1,....PRED_1_N] , .... [PRED_M_0,PRED_M_1,....PRED_M_N]] WHERE EACH DIFFERENT CATEGORY HAS A PREDICTION
#    [[SCORE_PROLOG_0,SCORE_HASKELL_0],[SCORE_PROLOG_1,SCORE_HASKELL_1] , .... , [SCORE_PROLOG_M,SCORE_HASKELL_M] ]
#
def make_predictionswithgrades(userDictionary, gradeDictionary, categoryDictionary, categories):
    outputPredictions = []
    outputScores = []
    categoryList = list(categories)
    for user in userDictionary:
        userScore = [0 for _ in range(len(categories))]  # [ 0_0 , 0_1 , ... , 0_N ]
        userSet = set()
        opl_id = userDictionary[user][0][1]
        lenList = len(userDictionary[user][0])
        maxProperties = lenList - 3
        for mylist in userDictionary[user]:  # This will be a list [CAT_i , .... , LANGUAGE_i]
            category = mylist[0]
            userSet.add(category)
            thisDecisionTree = categoryDictionary[category]
            forDecisionTree = mylist[1:-1]  # list [ PROPERTY_0, ... , PROPERTY_N]
            treePrediction = thisDecisionTree.predict([forDecisionTree])  # This will be the prediction.
            userScore[categoryList.index(category)] = treePrediction[0]
        remainingSet = categories - userSet
        for category in remainingSet:
            forDecisionTree = [opl_id] + [0 for _ in range(maxProperties)]
            treePrediction = categoryDictionary[category].predict([forDecisionTree])
            userScore[categoryList.index(category)] = treePrediction[0]
        outputPredictions.append(userScore)
        outputScores.append(gradeDictionary[user])
    return (outputPredictions, outputScores)


# TODO comments
def make_predictions_with_grades_in_df(decision_trees, dataframe, categoryList):
    outputPredictions = []
    outputScores = []
    for user in dataframe['user_id'].unique():
        data_usr = dataframe.loc[dataframe['user_id'] == user].drop(['user_id'], axis=1)
        user_predictions = []
        for category in categoryList:
            data_cat = data_usr.loc[dataframe['category'] == category].drop(['category'], axis=1)

            if data_cat.empty:
                user_predictions.append(0)
            else:
                data_list = data_cat.drop(['language', 'score_prolog', 'score_haskell'], axis=1).values.tolist()
                if category in decision_trees.keys():
                    prediction = decision_trees[category].predict(data_list)[0]
                else:
                    prediction = 0
                user_predictions.append(prediction)

        outputPredictions.append(user_predictions)
        outputScores.append(data_usr[['score_prolog', 'score_haskell']].iloc[0].tolist())
    return (outputPredictions, outputScores)
