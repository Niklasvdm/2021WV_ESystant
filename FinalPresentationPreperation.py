import math

import numpy as np
import time
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
    return sum([abs(prediction[x][0][y] - actual[x][y]) for x in range(len(prediction)) for y in
         range(len(prediction[0][0]))]) / (2 * len(prediction)), \
           sum([abs(prediction[x][0][0] + prediction[x][0][1] - actual[x][0] - actual[x][1]) for x in
                range(len(prediction))]) / (2 * len(prediction))


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

def runBoostingRegressorWithSubstrings(amount_of_runs, grades, query_result, big_dict):

    df = DataFrame(columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("S run number " + str(x+1))
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
        language_lists_prediction = []
        language_lists_actual = []
        for language in range(2, 0, -1):
            possible_categories = query_result.query('language==' + str(language))['category'].unique()

            my_boosting_trees = TreeConstructor.build_big_language_boostingtree_with_dataframe(
                data_points_training_df, possible_categories, language)
            # this function returns a dictionary containing the trained decision-trees having the categories as key.

            predicted_list, actual_verification = TreeConstructor.make_language_boosting_predictions_with_grades_in_df(
                my_boosting_trees, data_points_verification_df, possible_categories, language)
            predicted_list = [x[0][language % 2] for x in predicted_list]
            language_lists_prediction.append(predicted_list)
            language_lists_actual.append(actual_verification)
            """
            pass_fail_result = [(predicted_list[x] >= 5 and actual_verification[x] >= 5)
                            or (predicted_list[x] < 5 and actual_verification[x] < 5) for x in
                            range(len(predicted_list))]  # here we calculate all data we need
            total_avg_deviation += sum([abs(predicted_list[x] - actual_verification[x]) for x in
                                        range(len(predicted_list))]) / len(predicted_list)
            if (language == 1):
                total_haskell += sum(pass_fail_result)
            else:
                total_prolog += sum(pass_fail_result)
            """
        for xx in range(0, len(language_lists_prediction), 2):
            dfx = DataFrame({'Predicted Prolog': language_lists_prediction[xx]})
            dfx['Predicted Haskell'] = language_lists_prediction[xx + 1]
            dfx['Actual Prolog'] = language_lists_actual[xx]
            dfx['Actual Haskell'] = language_lists_actual[xx + 1]
            df = concat([df, dfx])
    return df

def runBoostingRegressorWithSubstrings_and_Times(amount_of_runs, grades, query_result, big_dict):

    df = DataFrame(columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    for x in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("ST run number " + str(x+1))
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
        language_lists_prediction = []
        language_lists_actual = []
        for language in range(2, 0, -1):
            possible_categories = query_result.query('language==' + str(language))['category'].unique()

            my_boosting_trees = TreeConstructor.build_big_boostingtree_with_dataframe(data_points_training_df,
                                                                                      possible_categories)
            # this function returns a dictionary containing the trained decision-trees having the categories as key.

            predicted_list, actual_verification = TreeConstructor.make_boosting_predictions_with_grades_in_df(
                my_boosting_trees, data_points_verification_df, possible_categories, language)
            predicted_list = [x[0][language % 2] for x in predicted_list]
            language_lists_prediction.append(predicted_list)
            language_lists_actual.append(actual_verification)
            """
            pass_fail_result = [(predicted_list[x] >= 5 and actual_verification[x] >= 5)
                            or (predicted_list[x] < 5 and actual_verification[x] < 5) for x in
                            range(len(predicted_list))]  # here we calculate all data we need
            total_avg_deviation += sum([abs(predicted_list[x] - actual_verification[x]) for x in
                                        range(len(predicted_list))]) / len(predicted_list)
            if (language == 1):
                total_haskell += sum(pass_fail_result)
            else:
                total_prolog += sum(pass_fail_result)
            """

        for xx in range(0, len(language_lists_prediction), 2):
            dfx = DataFrame({'Predicted Prolog': language_lists_prediction[xx]})
            dfx['Predicted Haskell'] = language_lists_prediction[xx + 1]
            dfx['Actual Prolog'] = language_lists_actual[xx]
            dfx['Actual Haskell'] = language_lists_actual[xx + 1]
            df = concat([df, dfx])
    return df


def runBoostingRegressorWithSubstrings_k_cross_validation(amount_of_runs, k, grades, query_result, big_dict):
    # preprocessing(host_name, root_name, passw_root, database_name, Queries.get_query_06_)
    df = DataFrame(columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    ################################################################## CROSS VALIDATION
    for i in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("SK Run number " + str(i + 1))

        alldata: [] = split_dataset(grades, k)

        for x in range(k):
            print("K Run number" + str(x + 1))
            (train_df,verification_df) = get_remaining_dataset(alldata, x)
            #################################################################
            # we drop the sample that we have selected to retain 90% to train

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

            language_lists_prediction = []
            language_lists_actual = []
            for language in range(2, 0, -1):
                possible_categories = query_result.query('language==' + str(language))['category'].unique()

                my_boosting_trees = TreeConstructor.build_big_boostingtree_with_dataframe(data_points_training_df,
                                                                                          possible_categories)
                # this function returns a dictionary containing the trained decision-trees having the categories as key.

                predicted_list, actual_verification = TreeConstructor.make_boosting_predictions_with_grades_in_df(
                    my_boosting_trees, data_points_verification_df, possible_categories, language)

                predicted_list = [x[0][language % 2] for x in predicted_list]
                language_lists_prediction.append(predicted_list)
                language_lists_actual.append(actual_verification)
                """
                pass_fail_result = [(predicted_list[x] >= 5 and actual_verification[x] >= 5)
                                or (predicted_list[x] < 5 and actual_verification[x] < 5) for x in
                                range(len(predicted_list))]  # here we calculate all data we need
                total_avg_deviation += sum([abs(predicted_list[x] - actual_verification[x]) for x in
                                            range(len(predicted_list))]) / len(predicted_list)
                if (language == 1):
                    total_haskell += sum(pass_fail_result)
                else:
                    total_prolog += sum(pass_fail_result)
                """

            for xx in range(0, len(language_lists_prediction), 2):
                dfx = DataFrame({'Predicted Prolog': language_lists_prediction[xx]})
                dfx['Predicted Haskell'] = language_lists_prediction[xx + 1]
                dfx['Actual Prolog'] = language_lists_actual[xx]
                dfx['Actual Haskell'] = language_lists_actual[xx + 1]
                df = concat([df, dfx])
    return df

def runBoostingRegressorWithSubstrings_and_Times_k_cross_validation(amount_of_runs, k, grades, query_result, big_dict):

    # preprocessing(host_name, root_name, passw_root, database_name, Queries.get_query_06_)
    df = DataFrame(columns=["Predicted Prolog", "Predicted Haskell", "Actual Prolog", "Actual Haskell"])
    ################################################################## CROSS VALIDATION
    for i in range(amount_of_runs):  # in this loop the experiment gets repeated
        print("ST Run number " + str(i + 1))

        alldata: [] = split_dataset(grades, k)

        for x in range(k):
            print("K Run number" + str(x + 1))
            (train_df,verification_df) = get_remaining_dataset(alldata, x)
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
            language_lists_prediction = []
            language_lists_actual = []
            for language in range(2, 0, -1):
                possible_categories = query_result.query('language==' + str(language))['category'].unique()

                my_boosting_trees = TreeConstructor.build_big_boostingtree_with_dataframe(data_points_training_df,
                                                                                          possible_categories)
                # this function returns a dictionary containing the trained decision-trees having the categories as key.

                predicted_list, actual_verification = TreeConstructor.make_boosting_predictions_with_grades_in_df(
                    my_boosting_trees, data_points_verification_df, possible_categories, language)

                predicted_list = [x[0][language % 2] for x in predicted_list]
                language_lists_prediction.append(predicted_list)
                language_lists_actual.append(actual_verification)
                """
                pass_fail_result = [(predicted_list[x] >= 5 and actual_verification[x] >= 5)
                                or (predicted_list[x] < 5 and actual_verification[x] < 5) for x in
                                range(len(predicted_list))]  # here we calculate all data we need
                total_avg_deviation += sum([abs(predicted_list[x] - actual_verification[x]) for x in
                                            range(len(predicted_list))]) / len(predicted_list)
                if (language == 1):
                    total_haskell += sum(pass_fail_result)
                else:
                    total_prolog += sum(pass_fail_result)
                """

            for xx in range(0, len(language_lists_prediction), 2):
                dfx = DataFrame({'Predicted Prolog': language_lists_prediction[xx]})
                dfx['Predicted Haskell'] = language_lists_prediction[xx + 1]
                dfx['Actual Prolog'] = language_lists_actual[xx]
                dfx['Actual Haskell'] = language_lists_actual[xx + 1]
                df = concat([df, dfx])

            ## END INNER K-CROSS VALIDATION LOOP

        # END AMOUNt_OF_RUNS LOOP
    return df


if __name__ == "__main__":
    host, root, passw = Database_Functions.MaxConnectivity()
   # host, root, passw = Database_Functions.NiklasConnectivity()
    sheetLocation = "/Users/informatica/Desktop/BPExcel/"
    amount_of_runs = 300
    k = 10
    databases = ["esystant1617","esystant1718","esystant1819","esystant1920","esystant1920"]
    queries = [Queries.get_query_09_1617_all_timestamp(),Queries.get_query_09_1718_all_timestamp(),
               Queries.get_query_09_1819_all_timestamp(),Queries.get_query_08_1920_all_timestamp(),
               Queries.get_query_08_1920_all_timestamp()]
    q2s = [Queries.get_query_08_rest_dropped_attributes_df,Queries.get_query_08_rest_dropped_attributes_df,
           Queries.get_query_08_rest_dropped_attributes_df, Queries.get_query_08_rest_dropped_attributes_df,
           Queries.get_query_08_1920_dropped_attributes_df]
    for x in range(len(databases)):
        query_result = Database_Functions.query_database_dataframe(host, root, passw, databases[x], queries[x])
        # this is a dataframe with the needed data
        query_result, big_dict, time_dict = preprocessing_2(query_result)

        query_result = pandasql.sqldf(q2s[x]("query_result"), locals())

        grades = query_result[['user_id', 'score_prolog', 'score_haskell']].drop_duplicates(subset='user_id')
        # this is a dataframe with all user_id's and all scores
        grades.reset_index(drop=True, inplace=True)  # we reset the number index of the dataframe (purely cosmetics)
        # selecting only prolog as cat
        # possible_categories = query_result['category'].unique()
        query_result_time = integrate_times_into_df(time_dict, query_result)

        run_results = runBoostingRegressorWithSubstrings(amount_of_runs, grades, query_result, big_dict)
        run_results.to_excel(sheetLocation + databases[x] +"-"+str(x)+ "BTWS.xlsx")

        run_results = runBoostingRegressorWithSubstrings_and_Times(amount_of_runs, grades, query_result_time, big_dict)
        run_results.to_excel(sheetLocation + databases[x] + "-"+str(x)+"BTWSAT.xlsx")

        run_results = runBoostingRegressorWithSubstrings_k_cross_validation(math.ceil(amount_of_runs/k), k, grades, query_result, big_dict)
        run_results.to_excel(sheetLocation + databases[x] +"-"+str(x)+ "BTWSKC.xlsx")

        run_results = runBoostingRegressorWithSubstrings_and_Times_k_cross_validation(math.ceil(amount_of_runs/k), k, grades, query_result_time, big_dict)
        run_results.to_excel(sheetLocation + databases[x] + "-"+str(x)+"BTWSATKC.xlsx")

