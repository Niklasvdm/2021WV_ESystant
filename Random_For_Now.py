from Database_Functions import create_database_connection
from Blob_File_Analysis import byteToLines, bytesToLines
from collections import Counter


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

    dict_total = {key: {} for key in big_dict[list(big_dict.keys())[0]].keys()}

    for user in training_users:
        for lan in big_dict[user]:

            value = big_dict[user][lan]
            subset[user] = value
            for cat in value:
                if cat in dict_total[lan].keys():
                    dict_total[lan][cat] += big_dict[user][lan][cat]
                else:
                    dict_total[lan][cat] = big_dict[user][lan][cat]

    return subset, dict_total
