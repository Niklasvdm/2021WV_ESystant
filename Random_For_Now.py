from Database_Functions import create_database_connection
from Blob_File_Analysis import byteToLines, bytesToLines
from collections import Counter
import pandas



# TODO comments fixen of dingen deleten
# Functie krijgt query als input die ~~~~~~~~1 FILE ~~~~~~~~ ophaalt en die naar een rij van lijnen
# omzet. Kan ook makkelijk geprint worden met printLines


# We moeten onze databases dezelfde naam geven want bij mij is dat Esystant_19_20 en we zouden ook best
# eenzelfde passwoord gebruiken
from ErrorFiles.StudentAnalyser import analyseByStudent,analyse_by_student_wtih_time


def queryToLines(query):
    db = create_database_connection("localhost", "root", "", "esystant1920")
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return byteToLines(result)


def queryMultipleResultsToLines(query):
    db = create_database_connection("localhost", "root", "", "esystant1920")
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return bytesToLines(result)


def getResultsFromDataBase(query, database):
    db = create_database_connection("localhost", "root", "", database)
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return bytesToLines(result)


def databaseToLines(localhost, root, password, database, query):
    db = create_database_connection(localhost, root, password, database)
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return bytesToLines(result)


# sql_prompt = "SELECT result_id,submission_id FROM results where result_id BETWEEN 41309 AND 41312 ;"
# printMultipleLines(queryMultipleResultsToLines(sql_prompt))

def make_count_dict(list_sequences, length_subsequence):
    # list_sequences is list of combination of characters (=string) in order of the time series
    # length_subsequence is the length of substring that is tracked
    return Counter([a[i:j] for a in list_sequences for i in range(len(a)) for j in
                    range(i + 1, len(a) + 1) if len(a[i:j]) == length_subsequence])


def somefunct(listofsets, length):
    subsets = []
    for x in range(len(listofsets) - length + 1):
        subs = []
        for y in range(length):
            if len(subs) == 0:
                subs = list(listofsets[x])
            else:
                temp = []
                for a in listofsets[x + y]:
                    for z in range(len(subs)):
                        temp.append(subs[z] + a)
                subs = temp
        subsets += subs
    return Counter(subsets)

def get_subfreq(dict_, length=3):
    subsets_all = {key: {} for key in dict_}
    for lan in dict_:
        for cat in dict_[lan]:
            subsets_cat = [Counter()]
            for oefening in dict_[lan][cat]:
                subsets = []
                if len(oefening)<length:
                    subsets = [''.join([error for compile_ev in oefening for error in compile_ev])]
                else:
                    for x in range(len(oefening) - length + 1):
                        subs = []
                        for y in range(length):
                            if len(subs) == 0:
                                subs = list(oefening[x])
                            else:
                                temp = []
                                for a in oefening[x + y]:
                                    for z in range(len(subs)):
                                        temp.append(subs[z] + a)
                                subs = temp
                        subsets += subs
                subsets_cat.append(Counter(subsets))
            sum_count = sum_counters(subsets_cat)
            subsets_all[lan][cat] = sum_count
    return subsets_all

def sum_counters(list_c):
    sum_c = list_c[0]
    if len(list_c)>1:
        for counter in list_c[1:]:
            sum_c += counter
    return sum_c

def preprocessing(query_result):
    big_dict = {}
    for student in query_result['user_id'].unique():
        error_list = analyseByStudent(query_result[['user_id','compile_errors','category','assignment_id','language','nb_failed']].loc[query_result['user_id'] == student].drop(['user_id'], axis=1))
        big_dict[student] = get_subfreq(error_list)
    return query_result,big_dict


def preprocessing_2(query_result):
    big_dict = {}
    big_time_dict = {}
    for student in query_result['user_id'].unique():
        error_list,time_dict = analyse_by_student_wtih_time(query_result[['user_id','compile_errors','category','assignment_id','language','nb_failed','nb_notimplemented','timestamp']].loc[query_result['user_id'] == student].drop(['user_id'], axis=1))
        big_dict[student] = get_subfreq(error_list)
        big_time_dict[student] = time_dict
    return query_result,big_dict,big_time_dict

def get_relevant_subset(training_users, big_dict):
    subset = {}

    dict_total = {1: {}, 2: {}}

    for user in training_users:
        subset[user] = {}
        for lan in big_dict[user]:

            value = big_dict[user][lan]
            subset[user].update(value)
            for cat in value:
                if cat in dict_total[lan].keys():
                    dict_total[lan][cat] += big_dict[user][lan][cat]
                else:
                    dict_total[lan][cat] = big_dict[user][lan][cat]

    return subset, dict_total

def add_freq_predictions_to_df(trees, data_points_df, frequency_list_df):
    new_col = []

    for index, row in data_points_df.iterrows():
        category = row['category']
        if category in trees.keys():
            predicted_score = trees[category].predict([frequency_list_df[row['user_id']][category]])
        else:
            predicted_score = [-1]
        new_col.append(predicted_score[0])
    data_points_df["Predicted_with_Freq"] = new_col

    return data_points_df

def make_frequency_list_df(big_dict, verification_users,total_freq_subset):
    frequency_list_df = {}
    for lan in total_freq_subset.keys():
        for category in total_freq_subset[lan].keys():
            list_possible_patterns = list(total_freq_subset[lan][category].keys())
            features = []
            for user in verification_users:
                if user not in frequency_list_df.keys():
                    frequency_list_df[user] = {}
                if category in big_dict[user][lan].keys():
                    list_specific_freq = [big_dict[user][lan][category][x] for x in list_possible_patterns]
                    frequency_list_df[user][category] = list_specific_freq
                    features.append(list_specific_freq)
    return frequency_list_df

def integrate_times_into_df(dictionary_times_and_hops,df):
    df: pandas.DataFrame
    dictionary_times_and_hops : {}
    hops : [int] = []
    resolveTime : [int] = []
    row_length = df.shape[1]
    for index,row in df.iterrows():
        user = row['user_id']
        category = row['category']
        Category_dict = dictionary_times_and_hops[user]
        if category in Category_dict.keys():
            (_hops,_time) = Category_dict[category]
        else:
            (_hops,_time) = (-1,-1)
        hops.append(_hops)
        resolveTime.append(_time)
    df.insert(row_length - 2 , 'hops',hops)
    df.insert(row_length - 2 , 'resolvetime',resolveTime)
    #df['hops'] = hops
    #df['resolvetime'] = resolveTime
    return df

