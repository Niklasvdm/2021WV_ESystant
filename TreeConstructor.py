from random import shuffle

from sklearn import tree
from sklearn import ensemble
from sklearn.multioutput import MultiOutputRegressor


########################################################################################################################
#   FUNCTIONS:
#
#   ~ splitBase
#
#           INPUT: Dictionary
#           OUTPUT: (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
#
#
#   ~ prepare_categories
#
#           REQUIREMENT: EERSTE PLAATS IN DICTIONARY USER IS CATEGORIE,LAATSTE PLAATS IS TAAL.
#                        GRADESDICTIONARY KOMT OVEREEN MET [PUNT_PROLOG,PUNT_HASKELL]
#           INPUT : { USER : [[CAT_0,...,LANGUAGE],[CAT_1,...,LANGUAGE],...]] , .... }
#                   { USER : [GRADE_PROLOG,GRADE_HASKELL],... }
#           OUTPUT : { ( CATEGORY_0 : [ [PROPERTY_0,PROPERTY_1,....],[PROPERTY_0,PROPERTY_1,...] ] ) , ( ...) , ....}
#                    { ( CATEGORY_0 : [ GRADE_0_0,GRADE_0_1,...] ) , ( CATEGORY_1 : [ GRADE_1_0,GRADE_1_1,...] ) , ... }
#
#
#   ~ buildTrees
#
#           INPUT: { CATEGORY_0 : [ LIST_0_0 , LIST_0_1 , ... LIST_0,N0] , CATEGORY_1 :
#                       [ LIST_1_0 , LIST_1_1 , ... LIST_1,N1]  , .... }
#                   { CATEGORY_0 : [ GRADE_0_0 , GRADE_0_1 , ... GRADE_0,N0] , CATEGORY_1 :
#                       [ GRADE_1_0 , GRADE_1_1 , ... GRADE_1,N1]  , .... }
#           OUTPUT: { CATEGORY_0 : DECISION_TREE_0  , CATEGORY_1 : DECISION_TREE_1  , ... }
#
#
#   ~ build_trees_with_dataframe
#
#           INPUT: Dictionary
#           OUTPUT: (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
#
#
#   ~ make_predictionswithgrades
#
#           input:  Dictionary of users and properties , Dictionary of users and their scores ,
#                   Dictionary with categories and trees, possible categories.
#                   { USER : [CATEGORY_ID, OPL_ID, ... , LANGUAGE] }
#
#           OUTPUT: [[PRED_0_0,PRED_0_1,....PRED_0_N],[PRED_1_0,PRED_1_1,....PRED_1_N] , ....
#                   [PRED_M_0,PRED_M_1,....PRED_M_N]] WHERE EACH DIFFERENT CATEGORY HAS A PREDICTION
#                   [[SCORE_PROLOG_0,SCORE_HASKELL_0],[SCORE_PROLOG_1,SCORE_HASKELL_1] , .... ,
#                   [SCORE_PROLOG_M,SCORE_HASKELL_M] ]
#
#
#   ~ make_predictions_with_grades_in_df
#
#           INPUT: Dictionary
#           OUTPUT: (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
########################################################################################################################

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


########################################################################################################################
# Nu willen we gewoon een functie kunnen geven dat een query ( en de nodige informatie neemt als input) en het resultaat
# van de decision tree meegeeft. Dit wordt eventueel gedaan met verschillende hulpfuncties. Om dit te doen werken:
#   1e kolom user id, 2e kolom per oefenzitting , laatste 2 kolommen Prolog & Haskell Respectively.
########################################################################################################################


# Function that per Category, makes a dictionary with all of the user necessairy and a list with the necessairy grades
#       REQUIREMENT: EERSTE PLAATS IN DICTIONARY USER IS CATEGORIE,LAATSTE PLAATS IS TAAL.
#                       GRADESDICTIONARY KOMT OVEREEN MET [PUNT_PROLOG,PUNT_HASKELL]
#       INPUT : { USER : [[CAT_0,...,LANGUAGE],[CAT_1,...,LANGUAGE],...]] , .... }
#               { USER : [GRADE_PROLOG,GRADE_HASKELL],... }
#       OUTPUT : { ( CATEGORY_0 : [ [PROPERTY_0,PROPERTY_1,....],[PROPERTY_0,PROPERTY_1,...] ] ) , ( ...) , ....}
#                { ( CATEGORY_0 : [ GRADE_0_0,GRADE_0_1,...] ) , ( CATEGORY_1 : [ GRADE_1_0,GRADE_1_1,...] ) , ... }
#
#
def prepare_categories(test_dictionary, grades_dictionary, categories, categories_and_language):
    exercise_dictionary = {}
    for number in categories: exercise_dictionary[number] = []
    exercise_grade_dictionary = {}
    for number in categories:  exercise_grade_dictionary[number] = []
    category_sets = [set(), set()]  # TODO : pas documentatie aan
    for users in test_dictionary:
        # ELKE USER HEEFT [[CAT_0,OPLEIDING_ID..,LANGUAGE],[CAT_1,OPLEIDING_ID...,LANGUAGE],...]
        oplID = test_dictionary[users][0][0]
        length_properties = len(test_dictionary[users][0]) - 3
        userSet = set()
        for user_list in test_dictionary[users]:
            language = user_list[-1] % 2  # 1 voor haskell, 0 voor Prolog.
            category_sets[int(language)].add(user_list[0])
            exercise_dictionary[user_list[0]].append(user_list[1:-1])
            userSet.add(user_list[0])
        remaining_categories = categories - userSet
        for i in remaining_categories:
            temp_list = [oplID] + [0 for _ in range(length_properties)]
            exercise_dictionary[i].append(temp_list)
        for [category, language] in categories_and_language:
            exercise_grade_dictionary[category].append(grades_dictionary[users][int(language % 2)])
    return exercise_dictionary, exercise_grade_dictionary, category_sets


# DOEL VAN BUILDTREES: we bouwen een boom per categorie met de nodige punten
#   INPUT: { CATEGORY_0 : [ LIST_0_0 , LIST_0_1 , ... LIST_0,N0] , CATEGORY_1 :
#           [ LIST_1_0 , LIST_1_1 , ... LIST_1,N1]  , .... }
#          { CATEGORY_0 : [ GRADE_0_0 , GRADE_0_1 , ... GRADE_0,N0] , CATEGORY_1 :
#           [ GRADE_1_0 , GRADE_1_1 , ... GRADE_1,N1]  , .... }
#   OUTPUT: { CATEGORY_0 : DECISION_TREE_0  , CATEGORY_1 : DECISION_TREE_1  , ... }
def buildTrees(dictionary_categories, dictionary_grades):
    decision_trees = {}
    for category in dictionary_categories.keys():
        clf = tree.DecisionTreeRegressor(max_depth=3)
        list_values = dictionary_categories[category]
        list_grades = dictionary_grades[category]
        decision_trees[category] = clf.fit(list_values, list_grades)
    return decision_trees


#   BUILD_TREES_WITH_DATAFRAME
#   This functions takes a dataframe and uses it to train decision-trees for each category
#   INPUT:  dataframe_to_train: the dataframe with data-points of each user per category
#   OUTPUT: decision_trees: a dictionary of trained decision-trees with categories as keys
def build_trees_with_dataframe(dataframe_to_train):
    decision_trees = {}
    for category in dataframe_to_train['category'].unique():
        clf = tree.DecisionTreeRegressor(max_depth=3)
        data_cat = dataframe_to_train.loc[dataframe_to_train['category'] == category].drop(['user_id', 'category'],
                                                                                           axis=1)
        language = int(data_cat.iloc[0]['language'] % 2)  # 1 voor haskell, 0 voor Prolog.

        list_values = data_cat.drop(['language', 'score_prolog', 'score_haskell'], axis=1).values.tolist()
        list_grades = [x[language] for x in data_cat[['score_prolog', 'score_haskell']].values.tolist()]
        decision_trees[category] = clf.fit(list_values, list_grades)
    return decision_trees


#   BUILD_BOOSTINGTREES_WITH_DATAFRAME
#   This function takes a dataframe and uses it to train Boosting decision trees on
#   Look at this ite for more information on use: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor
#   DATARAME : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
#   INPUT: [[USER_ID,CATEGORY,_,_,LANGUAGE,SCORE_PROLOG,SCORE_HASKELL]]
#   CONVERSIONS: [[USER,CATEGORY,_,_,LANGUAGE,SCORE_PROLOG,SCORE_HASKELL]] -> USR : [[CATEGORY,_,_,LANGUAGE,SCORE_PROLOG,SCORE_HASKELL]]
#   --> USR : CATEGORY : [_,_,LANGUAGE,SCORE_PROLOG,SCORE_HASKELL] OR   USR : CATEGORY : NULL
#   ---> USR : [CATEGORY,_,_,LANGUAGE] , USR : [SCORE_PROLOG,SCORE_HASKELL]
#   ----> DECISION TREE W/ [(usr_0):[CATEGORY_1,_,_,LANGUAGE,CATEGORY_2,_,_,LANGUAGE,...],
#                                   (usr_1):CATEGORY_1,_,_,LANGUAGE,CATEGORY_2,_,_,LANGUAGE,...]]
#   OUTPUT: DECISION TREES
#   DEFAULT VALUES: LEARNING_RATE = 0.1 , N_ESTIMATORS = 100 (higher = better most of the times) , MAX_DEPTH = 3 ,
def build_big_boostingtree_with_dataframe(dataframe_to_train, possibleCategories):
    boosting_tree = MultiOutputRegressor(
        ensemble.GradientBoostingRegressor(learning_rate=0.1, n_estimators=1000, max_depth=3))
    temp = dataframe_to_train.drop(['user_id', 'category', 'score_prolog', 'score_haskell'], axis=1)
    length = len((temp.head(1)).to_numpy()[0])
    for_tree = []
    grades_per_user = []
    for user in dataframe_to_train['user_id'].unique():  # We take for each user
        usr_list = []  # EACH USER WILL HAVE A LONG LIST OF ... # TODO
        data_usr = dataframe_to_train.loc[dataframe_to_train['user_id'] == user].drop(['user_id'],
                                                                                      axis=1)  # Don't know what axis does
        grades_user = data_usr.head(1).values.tolist()[0][-2:]
        for category in possibleCategories:
            data_cat = data_usr.loc[data_usr['category'] == category].drop(
                ['category', 'score_haskell', 'score_prolog'], axis=1)
            if data_cat.empty:
                temp = [category] + [-1 for _ in range(length)]
                usr_list += temp
            else:
                usr_list += [category] + data_cat.values.tolist()[0]
        grades_per_user.append(grades_user)  # TODO: THIS IS TEMP FIX
        for_tree.append(usr_list)
    boosting_tree.fit(for_tree, grades_per_user)
    return boosting_tree


# Purpose of next function -> Make a prediction with the testDict
# input: Dictionary of users and properties , Dictionary of users and their scores ,
#        Dictionary with categories and trees, possible categories.
#   { USER : [CATEGORY_ID, OPL_ID, ... , LANGUAGE] }
#
# OUTPUT:
#    [[PRED_0_0,PRED_0_1,....PRED_0_N],[PRED_1_0,PRED_1_1,....PRED_1_N] , ....
#       [PRED_M_0,PRED_M_1,....PRED_M_N]] WHERE EACH DIFFERENT CATEGORY HAS A PREDICTION
#    [[SCORE_PROLOG_0,SCORE_HASKELL_0],[SCORE_PROLOG_1,SCORE_HASKELL_1] , .... , [SCORE_PROLOG_M,SCORE_HASKELL_M] ]
#
def make_predictionswithgrades(user_dictionary, grade_dictionary, category_dictionary, categories):
    output_predictions = []
    output_scores = []
    category_list = list(categories)
    for user in user_dictionary:
        user_score = [0 for _ in range(len(categories))]  # [ 0_0 , 0_1 , ... , 0_N ]
        user_set = set()
        opl_id = user_dictionary[user][0][1]
        len_list = len(user_dictionary[user][0])
        max_properties = len_list - 3
        for mylist in user_dictionary[user]:  # This will be a list [CAT_i , .... , LANGUAGE_i]
            category = mylist[0]
            user_set.add(category)
            this_decision_tree = category_dictionary[category]
            for_decision_tree = mylist[1:-1]  # list [ PROPERTY_0, ... , PROPERTY_N]
            tree_prediction = this_decision_tree.predict([for_decision_tree])  # This will be the prediction.
            user_score[category_list.index(category)] = tree_prediction[0]
        remaining_set = categories - user_set
        for category in remaining_set:
            for_decision_tree = [opl_id] + [0 for _ in range(max_properties)]
            tree_prediction = category_dictionary[category].predict([for_decision_tree])
            user_score[category_list.index(category)] = tree_prediction[0]
        output_predictions.append(user_score)
        output_scores.append(grade_dictionary[user])
    return output_predictions, output_scores


#   MAKE_PREDICTIONS_WITH_GRADES_IN_DF
#   This functions takes a dictionary of decision-trees and data-points for each user for each category none or one
#   entry and predicts grades using the decision-trees.
#   INPUT:  decision_trees: a dictionary of decision-trees
#           dataframe: a dataframe of submissions of users per category and user
#   OUTPUT: output_predictions: a list of lists containing both predicted scores
#           output_scores: a list of lists containing both actual scores
def make_predictions_with_grades_in_df(decision_trees, dataframe):
    output_predictions = []
    output_scores = []
    for user in dataframe['user_id'].unique():
        data_usr = dataframe.loc[dataframe['user_id'] == user].drop(['user_id'], axis=1)
        user_predictions = []
        for category in decision_trees.keys():
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

        output_predictions.append(user_predictions)
        output_scores.append(data_usr[['score_prolog', 'score_haskell']].iloc[0].tolist())
    return output_predictions, output_scores


#   MAKE_PREDICTIONS_WITH_GRADES_IN_DF
#   This functions takes a dictionary of decision-trees and data-points for each user for each category none or one
#   entry and predicts grades using the decision-trees.
#   INPUT:  decision_trees: a deicsion tree
#           dataframe: a dataframe of submissions of users per category and user
#   OUTPUT: output_prediction: a list of lists containing predicted score
#           output_scores: a list of lists containing actual score
def make_boosting_predictions_with_grades_in_df(boosting_tree, dataframe, categories):
    output_predictions = []
    temp = dataframe.drop(['user_id', 'category', 'score_prolog', 'score_haskell'], axis=1)
    length = len((temp.head(1)).to_numpy()[0])
    for_tree = []
    output_scores = []
    for user in dataframe['user_id'].unique():  # We take for each user
        usr_list = []  # EACH USER WILL HAVE A LONG LIST OF ... # TODO
        data_usr = dataframe.loc[dataframe['user_id'] == user].drop(['user_id'], axis=1)  # Don't know what axis does
        grades_user = data_usr.head(1).values.tolist()[0][-2:]
        for category in categories:
            data_cat = data_usr.loc[data_usr['category'] == category].drop(
                ['category', 'score_haskell', 'score_prolog'], axis=1)
            if data_cat.empty:
                temp = [category] + [-1 for _ in range(length)]
                usr_list += temp
            else:
                usr_list += [category] + data_cat.values.tolist()[0]
        output_scores.append(grades_user)  # TODO: THIS IS TEMP FIX
        for_tree.append(usr_list)

    for array in for_tree:
        prediction = boosting_tree.predict([array])
        output_predictions.append(prediction)
    return output_predictions, output_scores


def build_boosting_trees_with_dataframe(dataframe_to_train):
    decision_trees = {}
    for category in dataframe_to_train['category'].unique():
        clf = ensemble.GradientBoostingRegressor(learning_rate=0.1, n_estimators=1000, max_depth=3)
        data_cat = dataframe_to_train.loc[dataframe_to_train['category'] == category].drop(['user_id', 'category'],
                                                                                           axis=1)
        language = int(data_cat.iloc[0]['language'] % 2)  # 1 voor haskell, 0 voor Prolog.

        list_values = data_cat.drop(['language', 'score_prolog', 'score_haskell'], axis=1).values.tolist()
        list_grades = [x[language] for x in data_cat[['score_prolog', 'score_haskell']].values.tolist()]

        decision_trees[category] = clf.fit(list_values, list_grades)
    return decision_trees
