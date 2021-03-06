import numpy as np
from sklearn import tree
from sklearn import ensemble
from sklearn.multioutput import MultiOutputRegressor

from pandas import DataFrame
import pandas

pandas.options.mode.chained_assignment = None  # default='warn'
from pandas import concat
import pandasql

import Database_Functions
import Queries
import TreeConstructor

import pydotplus

########################################################################################################################
#           THIS FILE SERVES THE PURPOSE OF RUNNING THE MAIN EXPERIMENT
########################################################################################################################
#   FUNCTIONS:
#
#       ~ pass_fail:
#           evaluation of the made predictions
#           INPUT:  prediction: a list containing lists of two predictions.
#                   actual: a list with the same length and structure as prediction, but with the actual correct data.
#           OUTPUT: A list of lists containing booleans and other lists with the structure
#                   [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...], where B is a boolean showing that the prediction and actual result
#                   are both over or both under the required threshold of 5/10
#
#
#       ~ average_deviation:
#           calculates the average deviation from the correct scores
#           INPUT:  prediction: a list containing lists of two predictions.
#                   actual: a list with the same length and structure as prediction, but with the actual correct data.
#           OUTPUT: the average deviation of type float of all numbers
#
#
#       ~ run:
#           runs the experiment x times
#           INPUT:  amount_of_runs: the amount of times you want to run the experiment, the variables that are
#                                   determined by the experiment are averaged.
#                   host_name: the name of the host used in connecting to the sql-server as a string.
#                   root_name: the name of the root-profile used in connecting to the sql-server as a string.
#                   database_name: the name of the database used in connecting to the sql-server as a string.
#                   query: the SQL-query as a string.
#           OUTPUT: - the average of correctly predicted results for both languages combined of all runs
#                   - the average of correctly predicted results for prolog of all runs
#                   - the average of correctly predicted results for haskell of all runs
#                   - the average deviation of all runs
#                   - the amount of predictions that were made
########################################################################################################################


# host,root,passw, sheetLocation = Database_Functions.NiklasConnectivity()
from Random_For_Now import preprocessing, get_relevant_subset, add_freq_predictions_to_df, \
    make_frequency_list_df, preprocessing_2, integrate_times_into_df

host, root, passw = Database_Functions.MaxConnectivity()  # , sheetLocation
#host,root,passw = Database_Functions.NiklasConnectivity()
my_tree_query = Queries.get_query_05()  # A SQL-querry in string
# The database that will be used
database1617 = "esystant1617"
database1718 = "esystant1718"
database1819 = "esystant1819"
database1920 = "esystant1920"
database = database1920


#   PASS_FAIL
#   This function evaluates given predictions with the actual score of a student. It will determine if the pass/fail
#   prediction per language was correct, and if the overall score prediction of pass/fail was correct. It returns a
#   list containing a list with two booleans: the first boolean showing if the prediction for prolog was correct,
#   the second showing if the prediction for haskell was correct. The second element of the list is if the overall score
#   was correct. This will be done for each prediction. The returned list will thus be [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...]
#   INPUT:  prediction: a list containing lists of two predictions.
#           actual: a list with the same length and structure as prediction, but with the actual correct data.
#   OUTPUT: A list of lists containing booleans and other lists with the structure [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...],
#           where B is a boolean showing that the prediction and actual result are both over or both under the required
#           threshold of 5/10
def pass_fail(prediction, actual):
    correct_scores = []
    for i in range(len(prediction)):
        result = [True, True]
        result_both = True
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
            result_both = False
        correct_scores.append([result, result_both])

    return correct_scores


#   AVERAGE_DEVIATION
#   This function calculates the average points the prediction was off.
#   INPUT:  prediction: a list containing lists of two predictions.
#           actual: a list with the same length and structure as prediction, but with the actual correct data.
#   OUTPUT: the average deviation of type float of all numbers
# TODO fix comments en hardcode y in tweede deel
def average_deviation(prediction, actual):
    return sum(
        [abs(prediction[x][y] - actual[x][y]) for x in range(len(prediction)) for y in range(len(prediction[0]))]) / (
                   2 * len(prediction)), sum(
        [abs(prediction[x][0] + prediction[x][1] - actual[x][0] - actual[x][1]) for x in range(len(prediction))]) / (
                   2 * len(prediction))


#   RUN
#   This function is the "main" function. This function runs the whole experiment. In the code you can see comments to
#   follow the logic.
#   INPUT:  amount_of_runs: the amount of times you want to run the experiment, the variables that are determined by the
#                           experiment are averaged.
#           host_name: the name of the host used in connecting to the sql-server as a string.
#           root_name: the name of the root-profile used in connecting to the sql-server as a string.
#           database_name: the name of the database used in connecting to the sql-server as a string.
#           query: the SQL-query as a string.
#   OUTPUT: - the average of correctly predicted results for both languages combined of all runs
#           - the average of correctly predicted results for prolog of all runs
#           - the average of correctly predicted results for haskell of all runs
#           - the average deviation of all runs
#           - the amount of predictions that were made
def run_decision_tree(amount_of_runs, host_name, root_name, passw_root, database_name, query):
    total_true = 0  # the amount of correctly predicted pass/fail of the sum of both languages.
    total_prolog = 0  # the amount of correctly predicted pass/fail of prolog.
    total_haskell = 0  # the amount of correctly predicted pass/fail of haskell.
    total_avg_deviation = 0  # the sum of the average deviation of each run.
    length_prediction_list = 1  # the amount of predictions made each run.
    total_avg_deviation_both = 0

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name,
                                                               query)  # this is a dataframe with the needed data
    grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
    # this is a dataframe with all user_id's and all scores
    grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)

    big_result_list = []

    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("run number " + str(x))
        verification_df = grades.sample(frac=0.1)  # this is a random selection of 10% of the dataframe
        train_df = grades.drop(verification_df.index)  # we drop the sample that we have selected to retain 90% to train

        training_users = set(train_df['user_id'].tolist())  # a set of all selected training-users

        data_points_training_df = query_result.iloc[np.where(query_result.user_id.isin(training_users))]
        # A dataframe of all submissions of the selected users.
        data_points_verification_df = query_result.drop(data_points_training_df.index)
        # we drop the selected training data to form the verification data

        my_decision_trees = TreeConstructor.build_trees_with_dataframe(data_points_training_df)
        # this function returns a dictionary containing the trained decision-trees having the categories as key.

        mega_tree_predictions, mega_tree_actual_scores = TreeConstructor.make_predictions_with_grades_in_df(
            my_decision_trees, data_points_training_df)
        #  this function returns two lists containing lists of grades in float. Predictions and Actual grades to compare

        combining_tree = tree.DecisionTreeRegressor(max_depth=3)
        my_mega_tree = combining_tree.fit(mega_tree_predictions, mega_tree_actual_scores)
        # we train a tree that learns how trustworthy predictions are for each category

        predicted_verification, actual_verification = TreeConstructor.make_predictions_with_grades_in_df(
            my_decision_trees, data_points_verification_df)
        # here we actually predict unseen data and also return the actual grades so we can compare later

        predicted_list = my_mega_tree.predict(predicted_verification).tolist()
        # we take the predictions and feed it to out combiner tree who knows what tree to trust

        pass_fail_result = pass_fail(predicted_list, actual_verification)  # here we calculate all data we need
        deviation = average_deviation(predicted_list, actual_verification)
        total_avg_deviation += deviation[0]
        total_avg_deviation_both += deviation[1]
        total_true += sum([x[1] for x in pass_fail_result])
        total_prolog += sum([x[0][0] for x in pass_fail_result])
        total_haskell += sum([x[0][1] for x in pass_fail_result])
        # we add all the parameters because at the end we will divide it by the total amount of runs
        if length_prediction_list != len(pass_fail_result):
            length_prediction_list = len(pass_fail_result)
        big_result_list += [predicted_list[x] + actual_verification[x] for x in range(len(predicted_list))]
    df = DataFrame(big_result_list,
                   columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])

    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / amount_of_runs, length_prediction_list, total_avg_deviation_both / amount_of_runs, df]


# run_results = run(10, host, root, passw, database1617, my_tree_query)
# print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
# print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
# print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
# print(str(run_results[3]) + " average deviation predictions")
#
# print("Ik ben Klaar")
########################################################################################################################
# New type of tree
########################################################################################################################
# TODO fix alle comments zodat ze weer kloppen

#   PASS_FAIL
#   This function evaluates given predictions with the actual score of a student. It will determine if the pass/fail
#   prediction per language was correct, and if the overall score prediction of pass/fail was correct. It returns a
#   list containing a list with two booleans: the first boolean showing if the prediction for prolog was correct,
#   the second showing if the prediction for haskell was correct. The second element of the list is if the overall score
#   was correct. This will be done for each prediction. The returned list will thus be [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...]
#   INPUT:  prediction: a list containing lists of two predictions.
#           actual: a list with the same length and structure as prediction, but with the actual correct data.
#   OUTPUT: A list of lists containing booleans and other lists with the structure [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...],
#           where B is a boolean showing that the prediction and actual result are both over or both under the required
#           threshold of 5/10
def pass_fail_boosting(prediction, actual):
    correct_scores = []
    for i in range(len(prediction)):
        result_both = True
        if ((prediction[i][0] < 10) and (actual[i] > 10)
                or ((prediction[i][0] > 10) and (actual[i] < 10))):
            result_both = False
        correct_scores.append([result_both])

    return correct_scores


#   PASS_FAIL
#   This function evaluates given predictions with the actual score of a student. It will determine if the pass/fail
#   prediction per language was correct, and if the overall score prediction of pass/fail was correct. It returns a
#   list containing a list with two booleans: the first boolean showing if the prediction for prolog was correct,
#   the second showing if the prediction for haskell was correct. The second element of the list is if the overall score
#   was correct. This will be done for each prediction. The returned list will thus be [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...]
#   INPUT:  prediction: a list containing lists of two predictions.
#           actual: a list with the same length and structure as prediction, but with the actual correct data.
#   OUTPUT: A list of lists containing booleans and other lists with the structure [[[Bp,Bh],Bt],[[Bp,Bh],Bt],...],
#           where B is a boolean showing that the prediction and actual result are both over or both under the required
#           threshold of 5/10
def pass_fail_boosting2(prediction, actual):
    correct_scores = []
    for i in range(len(prediction)):
        result = [True, True]
        result_both = True
        if ((prediction[i][0][0] > 5) and (actual[i][0] > 5)) or ((prediction[i][0][0] <= 5) and (actual[i][0] <= 5)):
            result[0] = result[0] and True
        else:
            result[0] = result[0] and False
        if ((prediction[i][0][1] > 5) and (actual[i][1] > 5)) or ((prediction[i][0][1] <= 5) and (actual[i][1] <= 0)):
            result[1] = result[1] and True
        else:
            result[1] = result[1] and False
        if ((prediction[i][0][0] + prediction[i][0][1] < 10) and (actual[i][0] + actual[i][1] > 10)
                or ((prediction[i][0][0] + prediction[i][0][1] > 10) and (actual[i][0] + actual[i][1] < 10))):
            result_both = False
        correct_scores.append([result, result_both])

    return correct_scores


#   AVERAGE_DEVIATION
#   This function calculates the average points the prediction was off.
#   INPUT:  prediction: a list containing lists of two predictions.
#           actual: a list with the same length and structure as prediction, but with the actual correct data.
#   OUTPUT: the average deviation of type float of all numbers
def average_deviation_boosting(prediction, actual):
    return sum(
        [abs(prediction[x][0] - actual[x]) for x in range(len(prediction))]) / (
                   2 * len(prediction))


#   AVERAGE_DEVIATION
#   This function calculates the average points the prediction was off.
#   INPUT:  prediction: a list containing lists of two predictions.
#           actual: a list with the same length and structure as prediction, but with the actual correct data.
#   OUTPUT: the average deviation of type float of all numbers
def average_deviation_boosting2(prediction, actual):
    return sum(
        [abs(prediction[x][0][y] - actual[x][y]) for x in range(len(prediction)) for y in
         range(len(prediction[0][0]))]) / (2 * len(prediction)), \
           sum(
               [abs(prediction[x][0][0] + prediction[x][0][1] - actual[x][0] - actual[x][1]) for x in
                range(len(prediction))]) / (
                   2 * len(prediction))


def runBoostingRegressor(amount_of_runs, host_name, root_name, passw_root, database_name, query):
    total_true = 0  # the amount of correctly predicted pass/fail of the sum of both languages.
    total_prolog = 0  # the amount of correctly predicted pass/fail of prolog.
    total_haskell = 0  # the amount of correctly predicted pass/fail of haskell.
    total_avg_deviation = 0  # the sum of the average deviation of each run.
    total_avg_deviation_both = 0
    length_prediction_list = 1  # the amount of predictions made each run.

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name,
                                                               query)  # this is a dataframe with the needed data
    grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
    # this is a dataframe with all user_id's and all scores
    grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)
    possible_categories = query_result.query('language==1')['category'].unique()
    # selecting only prolog as cat
    # possible_categories = query_result['category'].unique()

    big_result_list = []
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("run number " + str(x))
        verification_df = grades.sample(frac=0.1)  # this is a random selection of 10% of the dataframe
        train_df = grades.drop(verification_df.index)  # we drop the sample that we have selected to retain 90% to train

        training_users = set(train_df['user_id'].tolist())  # a set of all selected training-users

        data_points_training_df = query_result.iloc[np.where(query_result.user_id.isin(training_users))]
        # A dataframe of all submissions of the selected users.
        data_points_verification_df = query_result.drop(data_points_training_df.index)
        # we drop the selected training data to form the verification data

        my_boosting_trees = TreeConstructor.build_big_boostingtree_with_dataframe(data_points_training_df,
                                                                                  possible_categories)
        # this function returns a dictionary containing the trained decision-trees having the categories as key.

        predicted_list, actual_verification = TreeConstructor.make_boosting_predictions_with_grades_in_df(
            my_boosting_trees, data_points_verification_df, possible_categories)
        #  this function returns two lists containing lists of grades in float. Predictions and Actual grades to compare
        #        for x in range(len(predicted_list)):
        #            print(predicted_list[x][0])
        #            print(actual_verification[x])
        pass_fail_result = pass_fail_boosting2(predicted_list, actual_verification)
        # here we calculate all data we need
        deviation = average_deviation_boosting2(predicted_list, actual_verification)
        total_avg_deviation += deviation[0]
        total_avg_deviation_both += deviation[1]
        total_true += sum([x[1] for x in pass_fail_result])
        total_prolog += sum([x[0][0] for x in pass_fail_result])
        total_haskell += sum([x[0][1] for x in pass_fail_result])
        # we add all the parameters because at the end we will divide it by the total amount of runs
        if length_prediction_list != len(pass_fail_result):
            length_prediction_list = len(pass_fail_result)
        big_result_list += [predicted_list[x][0].tolist() + actual_verification[x] for x in range(len(predicted_list))]
    df = DataFrame(big_result_list,
                   columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / amount_of_runs, length_prediction_list, total_avg_deviation_both / amount_of_runs, df]


#   RUN
#   This function is the "main" function. This function runs the whole experiment. In the code you can see comments to
#   follow the logic.
#   INPUT:  amount_of_runs: the amount of times you want to run the experiment, the variables that are determined by the
#                           experiment are averaged.
#           host_name: the name of the host used in connecting to the sql-server as a string.
#           root_name: the name of the root-profile used in connecting to the sql-server as a string.
#           database_name: the name of the database used in connecting to the sql-server as a string.
#           query: the SQL-query as a string.
#   OUTPUT: - the average of correctly predicted results for both languages combined of all runs
#           - the average of correctly predicted results for prolog of all runs
#           - the average of correctly predicted results for haskell of all runs
#           - the average deviation of all runs
#           - the amount of predictions that were made
def run_boosting_regressor_cat_split(amount_of_runs, host_name, root_name, passw_root, database_name, query):
    total_true = 0  # the amount of correctly predicted pass/fail of the sum of both languages.
    total_prolog = 0  # the amount of correctly predicted pass/fail of prolog.
    total_haskell = 0  # the amount of correctly predicted pass/fail of haskell.
    total_avg_deviation = 0  # the sum of the average deviation of each run.
    length_prediction_list = 1  # the amount of predictions made each run.
    total_avg_deviation_both = 0

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name,
                                                               query)  # this is a dataframe with the needed data
    grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
    # this is a dataframe with all user_id's and all scores
    grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)

    big_result_list = []
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("run number " + str(x))
        verification_df = grades.sample(frac=0.1)  # this is a random selection of 10% of the dataframe
        train_df = grades.drop(verification_df.index)  # we drop the sample that we have selected to retain 90% to train

        training_users = set(train_df['user_id'].tolist())  # a set of all selected training-users

        data_points_training_df = query_result.iloc[np.where(query_result.user_id.isin(training_users))]
        # A dataframe of all submissions of the selected users.
        data_points_verification_df = query_result.drop(data_points_training_df.index)
        # we drop the selected training data to form the verification data

        my_boosting_trees = TreeConstructor.build_boosting_trees_with_dataframe(data_points_training_df)
        # this function returns a dictionary containing the trained decision-trees having the categories as key.

        example_boosting_trees = my_boosting_trees

        mega_tree_predictions, mega_tree_actual_scores = TreeConstructor.make_predictions_with_grades_in_df(
            my_boosting_trees, data_points_training_df)
        #  this function returns two lists containing lists of grades in float. Predictions and Actual grades to compare

        combining_tree = MultiOutputRegressor(ensemble.GradientBoostingRegressor(learning_rate=0.1, n_estimators=1000,
                                                                                 max_depth=3))
        my_mega_boosting_tree = combining_tree.fit(mega_tree_predictions, mega_tree_actual_scores)
        # we train a tree that learns how trustworthy predictions are for each category

        predicted_verification, actual_verification = TreeConstructor.make_predictions_with_grades_in_df(
            my_boosting_trees, data_points_verification_df)
        # here we actually predict unseen data and also return the actual grades so we can compare later

        predicted_list = my_mega_boosting_tree.predict(predicted_verification).tolist()
        # we take the predictions and feed it to out combiner tree who knows what tree to trust

        pass_fail_result = pass_fail(predicted_list, actual_verification)  # here we calculate all data we need
        deviation = average_deviation(predicted_list, actual_verification)
        total_avg_deviation += deviation[0]
        total_avg_deviation_both += deviation[1]
        total_true += sum([x[1] for x in pass_fail_result])
        total_prolog += sum([x[0][0] for x in pass_fail_result])
        total_haskell += sum([x[0][1] for x in pass_fail_result])
        # we add all the parameters because at the end we will divide it by the total amount of runs
        if length_prediction_list != len(pass_fail_result):
            length_prediction_list = len(pass_fail_result)
        big_result_list += [predicted_list[x] + actual_verification[x] for x in range(len(predicted_list))]
    df = DataFrame(big_result_list,
                   columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / amount_of_runs, length_prediction_list, total_avg_deviation_both / amount_of_runs,
            example_boosting_trees, df]


def run_boosting_regressor_language_split(amount_of_runs, host_name, root_name, passw_root, database_name, query):
    total_true = 0  # the amount of correctly predicted pass/fail of the sum of both languages.
    total_prolog = 0  # the amount of correctly predicted pass/fail of prolog.
    total_haskell = 0  # the amount of correctly predicted pass/fail of haskell.
    total_avg_deviation = 0  # the sum of the average deviation of each run.
    total_avg_deviation_both = 0
    length_prediction_list = 1  # the amount of predictions made each run.

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name,
                                                               query)  # this is a dataframe with the needed data
    grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
    # this is a dataframe with all user_id's and all scores
    grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)

    df = DataFrame(columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("run number " + str(x))
        verification_df = grades.sample(frac=0.1)  # this is a random selection of 10% of the dataframe
        train_df = grades.drop(verification_df.index)  # we drop the sample that we have selected to retain 90% to train

        training_users = set(train_df['user_id'].tolist())  # a set of all selected training-users

        data_points_training_df = query_result.iloc[np.where(query_result.user_id.isin(training_users))]
        # A dataframe of all submissions of the selected users.
        data_points_verification_df = query_result.drop(data_points_training_df.index)
        # we drop the selected training data to form the verification data

        language_lists_prediction = []
        language_lists_actual = []
        for language in range(2, 0, -1):
            possible_categories = query_result.query('language==' + str(language))['category'].unique()

            my_boosting_trees = TreeConstructor.build_big_language_boostingtree_with_dataframe(
                data_points_training_df, possible_categories, language)
            # this function returns a dictionary containing the trained decision-trees having the categories as key.

            predicted_list, actual_verification = TreeConstructor.make_language_boosting_predictions_with_grades_in_df(
                my_boosting_trees, data_points_verification_df, possible_categories, language)
            #  this function returns two lists containing lists of grades in float. Predictions and Actual grades to compare

            predicted_list = [x[0][language % 2] for x in predicted_list]
            pass_fail_result = [(predicted_list[x] > 5 and actual_verification[x] > 5)
                                or (predicted_list[x] < 5 and actual_verification[x] < 5) for x in
                                range(len(predicted_list))]  # here we calculate all data we need
            total_avg_deviation += sum([abs(predicted_list[x] - actual_verification[x]) for x in
                                        range(len(predicted_list))]) / len(predicted_list)
            if (language == 1):
                total_haskell += sum(pass_fail_result)
            else:
                total_prolog += sum(pass_fail_result)
            # we add all the parameters because at the end we will divide it by the total amount of runs
            if length_prediction_list != len(pass_fail_result):
                length_prediction_list = len(pass_fail_result)

            language_lists_prediction.append(predicted_list)
            language_lists_actual.append(actual_verification)
        for xx in range(0, len(language_lists_prediction), 2):
            dfx = DataFrame({'Predicted Prolog': language_lists_prediction[xx]})
            dfx['Predicted Haskell'] = language_lists_prediction[xx + 1]
            dfx['Actual Prolog'] = language_lists_actual[xx]
            dfx['Actual Haskell'] = language_lists_actual[xx + 1]
            df = concat([df, dfx])
    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / (2 * amount_of_runs), length_prediction_list,
            total_avg_deviation_both / amount_of_runs, df]


def runBoostingRegressorWithSubstrings(amount_of_runs, host_name, root_name, passw_root, database_name, query):
    total_true = 0  # the amount of correctly predicted pass/fail of the sum of both languages.
    total_prolog = 0  # the amount of correctly predicted pass/fail of prolog.
    total_haskell = 0  # the amount of correctly predicted pass/fail of haskell.
    total_avg_deviation = 0  # the sum of the average deviation of each run.
    total_avg_deviation_both = 0
    length_prediction_list = 1  # the amount of predictions made each run.

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name,
                                                               query)  # this is a dataframe with the needed data
    query_result, big_dict = preprocessing(query_result)

    query_result = pandasql.sqldf(Queries.get_query_08_1920_df("query_result"), locals())

    grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
    # this is a dataframe with all user_id's and all scores
    grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)
    possible_categories = query_result.query('language==1')['category'].unique()
    # selecting only prolog as cat
    # possible_categories = query_result['category'].unique()

    # preprocessing(host_name, root_name, passw_root, database_name, Queries.get_query_06_)
    big_result_list = []
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("run number " + str(x))
        verification_df = grades.sample(frac=0.1)  # this is a random selection of 10% of the dataframe
        train_df = grades.drop(verification_df.index)  # we drop the sample that we have selected to retain 90% to train

        training_users = set(train_df['user_id'].tolist())  # a set of all selected training-users
        verification_users = set(verification_df['user_id'].tolist())
        relevant_subset, total_freq_subset = get_relevant_subset(training_users, big_dict)
        trees, frequency_list_df_training = TreeConstructor.create_trees_with_subsets(train_df, relevant_subset,
                                                                                      total_freq_subset)
        data_points_training_df = query_result.iloc[np.where(query_result.user_id.isin(training_users))]
        # we have one boosting trees per category from create_trees_with_subsets, we now predict one score per
        # user and append this to the dataframe.
        data_points_training_df = add_freq_predictions_to_df(trees, data_points_training_df, frequency_list_df_training)
        frequency_list_df_ver = make_frequency_list_df(big_dict, verification_users, total_freq_subset)

        # A dataframe of all submissions of the selected users.
        data_points_verification_df = query_result.drop(data_points_training_df.index)
        # we drop the selected training data to form the verification data
        data_points_verification_df = add_freq_predictions_to_df(trees, data_points_verification_df,
                                                                 frequency_list_df_ver)
        my_boosting_trees = TreeConstructor.build_big_boostingtree_with_dataframe(data_points_training_df,
                                                                                  possible_categories)
        # this function returns a dictionary containing the trained decision-trees having the categories as key.

        predicted_list, actual_verification = TreeConstructor.make_boosting_predictions_with_grades_in_df(
            my_boosting_trees, data_points_verification_df, possible_categories)
        #  this function returns two lists containing lists of grades in float. Predictions and Actual grades to compare
        #        for x in range(len(predicted_list)):
        #            print(predicted_list[x][0])
        #            print(actual_verification[x])
        pass_fail_result = pass_fail_boosting2(predicted_list, actual_verification)
        # here we calculate all data we need
        deviation = average_deviation_boosting2(predicted_list, actual_verification)
        total_avg_deviation += deviation[0]
        total_avg_deviation_both += deviation[1]
        total_true += sum([x[1] for x in pass_fail_result])
        total_prolog += sum([x[0][0] for x in pass_fail_result])
        total_haskell += sum([x[0][1] for x in pass_fail_result])
        # we add all the parameters because at the end we will divide it by the total amount of runs
        if length_prediction_list != len(pass_fail_result):
            length_prediction_list = len(pass_fail_result)
        big_result_list += [predicted_list[x][0].tolist() + actual_verification[x] for x in range(len(predicted_list))]
    df = DataFrame(big_result_list,
                   columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / amount_of_runs, length_prediction_list, total_avg_deviation_both / amount_of_runs, df]


def runBoostingRegressorWithSubstrings_and_Times(amount_of_runs, host_name, root_name, passw_root, database_name,
                                                 query):
    total_true = 0  # the amount of correctly predicted pass/fail of the sum of both languages.
    total_prolog = 0  # the amount of correctly predicted pass/fail of prolog.
    total_haskell = 0  # the amount of correctly predicted pass/fail of haskell.
    total_avg_deviation = 0  # the sum of the average deviation of each run.
    total_avg_deviation_both = 0
    length_prediction_list = 1  # the amount of predictions made each run.

    query_result = Database_Functions.query_database_dataframe(host_name, root_name, passw_root, database_name,
                                                               query)  # this is a dataframe with the needed data
    query_result, big_dict, time_dict = preprocessing_2(query_result)

    query_result = pandasql.sqldf(Queries.get_query_09_1819_df("query_result"), locals())

    grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
    # this is a dataframe with all user_id's and all scores
    grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)
    possible_categories = query_result.query('language==1')['category'].unique()
    # gras = query result + Time Dict.
    query_result = integrate_times_into_df(time_dict, query_result)
    # selecting only prolog as cat
    # possible_categories = query_result['category'].unique()

    # preprocessing(host_name, root_name, passw_root, database_name, Queries.get_query_06_)
    big_result_list = []
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("run number " + str(x))
        verification_df = grades.sample(frac=0.1)  # this is a random selection of 10% of the dataframe
        train_df = grades.drop(verification_df.index)  # we drop the sample that we have selected to retain 90% to train

        training_users = set(train_df['user_id'].tolist())  # a set of all selected training-users
        verification_users = set(verification_df['user_id'].tolist())
        relevant_subset, total_freq_subset = get_relevant_subset(training_users, big_dict)
        trees, frequency_list_df_training = TreeConstructor.create_trees_with_subsets(train_df, relevant_subset,
                                                                                      total_freq_subset)
        data_points_training_df = query_result.iloc[np.where(query_result.user_id.isin(training_users))]
        # we have one boosting trees per category from create_trees_with_subsets, we now predict one score per
        # user and append this to the dataframe.
        data_points_training_df = add_freq_predictions_to_df(trees, data_points_training_df, frequency_list_df_training)
        frequency_list_df_ver = make_frequency_list_df(big_dict, verification_users, total_freq_subset)

        # A dataframe of all submissions of the selected users.
        data_points_verification_df = query_result.drop(data_points_training_df.index)
        # we drop the selected training data to form the verification data
        data_points_verification_df = add_freq_predictions_to_df(trees, data_points_verification_df,
                                                                 frequency_list_df_ver)
        my_boosting_trees = TreeConstructor.build_big_boostingtree_with_dataframe(data_points_training_df,
                                                                                  possible_categories)
        # this function returns a dictionary containing the trained decision-trees having the categories as key.

        predicted_list, actual_verification = TreeConstructor.make_boosting_predictions_with_grades_in_df(
            my_boosting_trees, data_points_verification_df, possible_categories)
        #  this function returns two lists containing lists of grades in float. Predictions and Actual grades to compare
        #        for x in range(len(predicted_list)):
        #            print(predicted_list[x][0])
        #            print(actual_verification[x])
        pass_fail_result = pass_fail_boosting2(predicted_list, actual_verification)
        # here we calculate all data we need
        deviation = average_deviation_boosting2(predicted_list, actual_verification)
        total_avg_deviation += deviation[0]
        total_avg_deviation_both += deviation[1]
        total_true += sum([x[1] for x in pass_fail_result])
        total_prolog += sum([x[0][0] for x in pass_fail_result])
        total_haskell += sum([x[0][1] for x in pass_fail_result])
        #

        # we add all the parameters because at the end we will divide it by the total amount of runs
        if length_prediction_list != len(pass_fail_result):
            length_prediction_list = len(pass_fail_result)
        big_result_list += [predicted_list[x][0].tolist() + actual_verification[x] for x in range(len(predicted_list))]
    df = DataFrame(big_result_list,
                   columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / amount_of_runs, length_prediction_list, total_avg_deviation_both / amount_of_runs, df]


amo_runs = 1
# Here we call the needed functions to initiate the experiment
run_results = run_decision_tree(amo_runs, host, root, passw, database1920, Queries.get_query_05())
print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[3]) + " average deviation single predictions")
print(str(run_results[5]) + " average deviation predictions both combined")

"""
amo_runs = 15
database = database1819
my_tree_query = Queries.get_query_05_1819()
# Here we call the needed functions to initiate the experiment
run_results = runBoostingRegressor(amo_runs,host,root,passw,database,my_tree_query)
#run_results = run_boosting_regressor_cat_split(1, host, root, passw, database, my_tree_query)
print("amount of runs: ", amo_runs, "with database: " + database + " gives the following predictions (boosting regressor):")
print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[3]) + " average deviation single predictions")
print(str(run_results[5]) + " average deviation predictions both combined")

run_results = run_boosting_regressor_cat_split(amo_runs,host,root,passw,database,my_tree_query)
print("amount of runs" , amo_runs , "with database" + database + "gives the following predictions (boosting regressor category split):")
print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[3]) + " average deviation single predictions")
print(str(run_results[5]) + " average deviation predictions both combined")

run_results = run_boosting_regressor_language_split(amo_runs,host,root,passw,database,my_tree_query)
print("amount of runs" , amo_runs , "with database" + database + "gives the following predictions (boosting regressor language split):")
print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
print(str(run_results[3]) + " average deviation single predictions")
print(str(run_results[5]) + " average deviation predictions both combined")
"""

# create excel sheets
"""
databasequery = [(database1617,Queries.get_query_05_1617()),(database1718,Queries.get_query_05_1718()),(database1819,Queries.get_query_05_1819())]
for (database, my_tree_query) in databasequery:
    run_results = run_boosting_regressor_language_split(400, host, root, passw, database, my_tree_query)
    print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[3]) + " average deviation single predictions")
    run_results[-1].to_excel(sheetLocation + database + "BTL.xlsx", sheet_name=str(run_results[0]) + "#" + str(run_results[1]) + "#" + str(
                                 run_results[2]) + "-" + str(run_results[4]) + "#" + str(run_results[3]))
    run_results = run_decision_tree(400, host, root, passw, database, my_tree_query)
    print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[3]) + " average deviation single predictions")
    run_results[-1].to_excel(sheetLocation+database+"DT.xlsx",sheet_name=str(run_results[0])+"#"+str(run_results[1])+"#"+str(run_results[2])+"-"+str(run_results[4])+"#"+str(run_results[3]))
    run_results = runBoostingRegressor(400, host, root, passw, database, my_tree_query)
    print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[3]) + " average deviation single predictions")
    run_results[-1].to_excel(sheetLocation+database+"BT.xlsx",sheet_name=str(run_results[0])+"#"+str(run_results[1])+"#"+str(run_results[2])+"-"+str(run_results[4])+"#"+str(run_results[3]))
    run_results = run_boosting_regressor_cat_split(400, host, root, passw, database, my_tree_query)
    print(str(run_results[0]) + " average total pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[1]) + " average prolog pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[2]) + " average haskell pass/fail correct, out of " + str(run_results[4]))
    print(str(run_results[3]) + " average deviation single predictions")
    run_results[-1].to_excel(sheetLocation+database+"BTC.xlsx",sheet_name=str(run_results[0])+"#"+str(run_results[1])+"#"+str(run_results[2])+"-"+str(run_results[4])+"#"+str(run_results[3]))


for x in run_results[6].keys():
    for i in range(0, 10):
        sub_tree = run_results[6][x].estimators_[i, 0]

        dot_data = tree.export_graphviz(
            sub_tree,
            out_file=None, filled=True,
            rounded=True,
            special_characters=True,
            proportion=True,
        )

        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_png("tree" + str(i) + ".png")
"""
