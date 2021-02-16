from sklearn import tree

import Database_Functions
import Queries
import TreeConstructor
import pandas as pd
import numpy as np

# host,root,passw = Database_Functions.NiklasConnectivity()
host, root, passw = Database_Functions.MaxConnectivity()

my_tree_query = Queries.getQuery05()
database = "esystant1920"


# queryResult = Database_Functions.query_database_dataframe(host,root,passw,database,my_tree_query)

# print(queryResult)


# for x in datapoints:
#    print(x + ': ' + str(len(datapoints[x])))
#    print(datapoints[x][0])


# Okay, we've got a dictionary with { KEY : VALUE } ,
#       KEY == CATEGORY
#       VALUE == DECISION TREE


# for i in range(len(megatreescores)):
#    print(megatreepredictions[i] , megatreescores[i])


#   TODO:       HEEFT DE PLAATSING DE NULLEN EFFECT OP EINDRESULTAAT
# [0 for _ in range(len(list)]
#  Category = c

#
#       INPUT: [[SCORE_PROLOG_0,SCORE_HASKELL_0],...]
#               [[SCORE_PROLOG_0,SCORE_HASKELL_0],...]
#
#
def pass_fail(prediction, actual):
    correctscores = []
    for i in range(len(prediction)):
        result = [True, True]
        resultboth = True
        if ((prediction[i][0] > 5) and (actual[i][0] > 5)) or ((prediction[i][0] <= 5) and (actual[i][0] <= 5)):
            result[0] = result[0] and True
        else:
            result[0] = result[0] and False
        if ((prediction[i][1] > 5) and (actual[i][1] > 5)) or ((prediction[i][1] <= 5) and (actual[i][1] <= 0)):
            result[1] = result[1] and True
        else:
            result[1] = result[1] and False
        if ((prediction[i][0] + prediction[i][1] < 10) and (actual[i][0] + actual[i][1] > 10)
                or ((prediction[i][0] + prediction[i][1] > 10) and (actual[i][0] + actual[i][1] < 10))):
            resultboth = False
        correctscores.append([result, resultboth])

    return correctscores


def average_deviation(prediction, actual):
    return sum(
        [abs(prediction[x][y] - actual[x][y]) for x in range(len(prediction)) for y in range(len(prediction[0]))]) / (
                   2 * len(prediction))


def run(amount_of_runs, host_name, root_name, passw_root, database_name, query):
    total_true = 0
    total_prolog = 0
    total_haskell = 0
    total_avg_deviation = 0
    length_prediction_list = 1

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name, query)
   # data_points, grades, categories, categories_and_languages = Database_Functions.groupByUserGradesAndCategories(
   #     query_result)

    grades = query_result[['user_id','score_prolog','score_haskell']].drop_duplicates(subset='user_id')
    grades.reset_index(drop=True, inplace=True)

    categories = query_result['category'].unique().tolist()



    for x in range(amount_of_runs):
        #test_dict, verification_dict = TreeConstructor.splitBase(data_points)
        verification_df = grades.sample(frac=0.1)
        test_df = grades.drop(verification_df.index)

        test_users = set(test_df['user_id'].tolist())
        #   verification_users = set(verification_df['user_id'].tolist())

        data_points_test_df = query_result.iloc[np.where(query_result.user_id.isin(test_users))]
        data_points_verification_df = query_result.drop(data_points_test_df.index)

        # print(data_points_test_df.to_string())

        #(categoryUsers, categoryGrades, splitCategories) = TreeConstructor.prepareCategories(test_dict, grades,
        #                                                                                     categories,
        #                                                                                    categories_and_languages)


        #my_decision_trees = TreeConstructor.buildTrees(categoryUsers, categoryGrades)


        my_decision_trees = TreeConstructor.buildTrees2(data_points_test_df)

        #megatree_predictions, megatree_scores = TreeConstructor.make_predictionswithgrades(test_dict, grades,
        #                                                                                   my_decision_trees,
        #                                                                                   categories)

        megatree_predictions, megatree_scores = TreeConstructor.make_predictionswithgrades2(my_decision_trees,data_points_test_df,categories)
        clf = tree.DecisionTreeRegressor(max_depth=3)
        my_mega_tree = clf.fit(megatree_predictions, megatree_scores)

        #(predictedVerification, actualVerification) = TreeConstructor.make_predictionswithgrades(verification_dict,
        #                                                                                         grades,
        #                                                                                         my_decision_trees,
        #                                                                                         categories)
        (predictedVerification, actualVerification) = TreeConstructor.make_predictionswithgrades2(my_decision_trees,data_points_verification_df,categories)
        predicted_list = my_mega_tree.predict(predictedVerification).tolist()
        pass_fail_result = pass_fail(predicted_list, actualVerification)
        total_avg_deviation += average_deviation(predicted_list, actualVerification)
        total_true += sum([x[1] for x in pass_fail_result])
        total_prolog += sum([x[0][0] for x in pass_fail_result])
        total_haskell += sum([x[0][1] for x in pass_fail_result])
        if length_prediction_list != len(pass_fail_result):
            length_prediction_list = len(pass_fail_result)
    return total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs, \
           total_avg_deviation / amount_of_runs, length_prediction_list


run_results = run(100, host, root, passw, database, my_tree_query)
print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[3]) + " average deviation predictions")
