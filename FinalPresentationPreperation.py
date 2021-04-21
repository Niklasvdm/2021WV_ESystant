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

# host,root,passw, sheetLocation = Database_Functions.NiklasConnectivity()
from Random_For_Now import preprocessing, get_relevant_subset, add_freq_predictions_to_df, \
    make_frequency_list_df, preprocessing_2, integrate_times_into_df

#host, root, passw = Database_Functions.MaxConnectivity()  # , sheetLocation
host,root,passw = Database_Functions.NiklasConnectivity()
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
def average_deviation_boosting2(prediction, actual):
    return sum(
        [abs(prediction[x][0][y] - actual[x][y]) for x in range(len(prediction)) for y in
         range(len(prediction[0][0]))]) / (2 * len(prediction)), \
           sum(
               [abs(prediction[x][0][0] + prediction[x][0][1] - actual[x][0] - actual[x][1]) for x in
                range(len(prediction))]) / (
                   2 * len(prediction))


def split_dataset(grades, k):
    alldata = []
    # alldata: [] = split_dataset(grades, k)

    percentage = 1 / k  # Percentage
    K_amount = len(grades) * percentage  # Exact amount

    while percentage < 1:
        temp = grades.sample(frac=percentage)  # this is a random selection of 10% of the dataframe
        grades = grades.drop(temp.index)
        grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)
        alldata.append(temp)  # we drop the sample that we have selected to retain 90% to train
        percentage = K_amount / len(grades)

    alldata.append(grades)
    return alldata


def get_remaining_dataset(Dataset, i):
    test: DataFrame = None
    validator: DataFrame = None
    for v in range(i):
        if validator is None:
            validator = Dataset[v]
        else:
            validator = concat([validator, Dataset[v]])
    test = (Dataset[i])
    for v in range(i + 1, len(Dataset)):
        if validator is None:
            validator = Dataset[v]
        else:
            validator = concat([validator, Dataset[v]])
    return (validator, test)

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


def runBoostingRegressorWithSubstrings_k_cross_validation(amount_of_runs,k, host_name, root_name, passw_root, database_name, query):
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
    ################################################################## CROSS VALIDATION

    for i in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("Run number " + str(i + 1))

        alldata: [] = split_dataset(grades, k)

        for x in range(k):
            print("K Run number" + str(x + 1))
            (verification_df, train_df) = get_remaining_dataset(alldata, x)
            #################################################################
            print("run number " + str(x)) # we drop the sample that we have selected to retain 90% to train

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

def runBoostingRegressorWithSubstrings_and_Times_k_cross_validation(amount_of_runs,k, host_name, root_name, passw_root, database_name,
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
    ################################################################## CROSS VALIDATION

    for i in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("Run number " + str(i + 1))

        alldata: [] = split_dataset(grades, k)

        for x in range(k):
            print("K Run number" + str(x + 1))
            (verification_df, train_df) = get_remaining_dataset(alldata, x)
            #################################################################
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
            ## END INNER K-CROSS VALIDATION LOOP

        # END AMOUNt_OF_RUNS LOOP
        df = DataFrame(big_result_list,
                       columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])

    return [total_true / amount_of_runs, total_prolog / amount_of_runs, total_haskell / amount_of_runs,
            total_avg_deviation / amount_of_runs, length_prediction_list, total_avg_deviation_both / amount_of_runs, df]