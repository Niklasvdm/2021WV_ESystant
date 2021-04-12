import Database_Functions
from Queries import *
from ErrorFiles.ErrorAnalysis import *
import Blob_File_Analysis
import datetime

host, root, passw = Database_Functions.NiklasConnectivity()
# host,root,passw = Database_Functions.MaxConnectivity()
database1617 = "esystant1617"
database1718 = "esystant1718"
database1819 = "esystant1819"
database1920 = "esystant1920"
database = database1920


def analyseByStudent(query_result):
    # myQuery = get_query_06()
    #
    #
    # query_result = Database_Functions.query_database_dataframe(host,root,passw,database,myQuery)
    # print(query_result)
    big_dict = {1: {}, 2: {}}
    for category in query_result['category'].unique():
        language = query_result.loc[query_result['category'] == category].drop(
            ['category', 'compile_errors', 'assignment_id', 'nb_failed'],
            axis=1).head(1).values.tolist()[0][0]
        category_df = query_result.loc[query_result['category'] == category].drop(['category'],
                                                                                  axis=1)
        byAssigmentProlog = []
        byAssigmentHaskell = []
        a = 0
        for assignment_id in category_df['assignment_id'].unique():
            files = category_df.loc[category_df['assignment_id'] == assignment_id].drop(['assignment_id', 'language'],
                                                                                        axis=1)

            my_files = files.values.tolist()

            if language == 1:
                byAssigmentHaskell.append(haskell_numerical_parser(my_files))
                big_dict[1][category] = byAssigmentHaskell
            else:
                byAssigmentProlog.append(prolog_numerical_parser(my_files))
                big_dict[2][category] = byAssigmentProlog

                # ["A" , B , C , D , D , A , 0 ]
                # for i in range( 0 ,  len(list()) - 2 )
                #       list[i] + list[i+1] + list[ i + 2]
                #

            a += 1
        # print("the category was: " + str(category) + " there were " + str(a) + " assignments"  + " and the error messages were: \n" , byAssigment)

    return big_dict


###
# 1e functie -> We geven student + oefz mee en we willen gewoon de opeenvolgende errors voor die oefz.
#
#
######


myQuery = get_query_06()

data = Database_Functions.query_database_dataframe(host, root, passw, database, myQuery)
#print(data)


def analyse_by_student_wtih_time(query_result):
    # analyseByStudent(data)
    big_dict = {1: {}, 2: {}}
    big_dict_time = {1: {}, 2: {}}
    for category in query_result['category'].unique():
        language = query_result.loc[query_result['category'] == category].drop(
            ['category', 'compile_errors', 'assignment_id', 'nb_failed', 'nb_notimplemented', 'timestamp'],
            axis=1).head(1).values.tolist()[0][0]
        category_df = query_result.loc[query_result['category'] == category].drop(['category'],
                                                                                  axis=1)
        byAssigmentProlog = []
        byAssigmentHaskell = []
        a = 0
        for assignment_id in category_df['assignment_id'].unique():
            files = category_df.loc[category_df['assignment_id'] == assignment_id].drop(
                ['assignment_id', 'language'],
                axis=1)

            my_files = files.values.tolist()
            # Contains Compile errors, nb_failed, nb_notimplemented,timestamp [[compile_errors,nb_failed,,nb_notimplemented,timestamp],[_,_,_]]
            i = 0
            hops = 0
            resolveTime: datetime
            initialTimeStamp: datetime
            finalTimeStamp: datetime
            finishedExercise = False
            lenList = len(my_files)
            i = 0
            for list in my_files:
                [_, nb_failed, nb_notimplemented, timestamp] = list
                timestamp = str(timestamp)
                if (i == 0):
                    initialTimeStamp = datetime.datetime(int(timestamp[:4]), int(timestamp[4:6]),
                                                         int(timestamp[6:8]), int(timestamp[8:10]),
                                                         int(timestamp[10:]))
                if (nb_notimplemented == 0 and nb_failed == 0 and not finishedExercise):
                    finalTimeStamp = datetime.datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]),
                                                       int(timestamp[8:10]), int(timestamp[10:]))
                    finishedExercise = True
                    hops = i + 1

                i += 1
            if not finishedExercise:
                hops = i + 1
                resolveTime = -1
                big_dict_time[category] = (-1,hops)
            else:
                resolveTime = finalTimeStamp - initialTimeStamp
                # resolveTime
                if language == 1:
                    big_dict_time[category] = ((resolveTime.total_seconds() / 60), hops)
                else:
                    big_dict_time[category] = ((resolveTime.total_seconds() / 60), hops)

            files = category_df.loc[category_df['assignment_id'] == assignment_id].drop(
                ['nb_notimplemented', 'timestamp'],
                axis=1)
            my_files = files.values.tolist()

            if language == 1:
                byAssigmentHaskell.append(haskell_numerical_parser(my_files))
                big_dict[1][category] = byAssigmentHaskell
                # IDGAF
            else:
                byAssigmentProlog.append(prolog_numerical_parser(my_files))
                big_dict[2][category] = byAssigmentProlog

                # ["A" , B , C , D , D , A , 0 ]
                # for i in range( 0 ,  len(list()) - 2 )
                #       list[i] + list[i+1] + list[ i + 2]
                #

            a += 1
        # print("the category was: " + str(category) + " there were " + str(a) + " assignments"  + " and the error messages were: \n" , byAssigment)
    return (big_dict, big_dict_time)

# myQuery = get_query_06()
#
#
# query_result = Database_Functions.query_database_dataframe(host,root,passw,database,myQuery)
# print(query_result)
# for category in query_result['category'].unique():
#     language = query_result.loc[query_result['category'] == category].drop(['category','compile_errors','assignment_id'],
#                                                                               axis=1).head(1).values.tolist()[0][0]
#     category_df = query_result.loc[query_result['category'] == category].drop(['category'],
#                                                                               axis=1)
#     byAssigment = []
#     a= 0
#     for assignment_id in category_df['assignment_id'].unique():
#         files = category_df.loc[category_df['assignment_id'] == assignment_id].drop(['assignment_id', 'language'],
#                                                                                       axis=1)
#
#         my_files = files.values.tolist()
#         if len(my_files) ==0:
#             print("oops, dan maar niet")
#         elif language == 1:
#             byAssigment.append(document_tfid_parser(my_files))
#         else:
#             byAssigment.append(document_tfid_parser(my_files))
#         a += 1
#     print("the category was: " + str(category) + " there were " + str(a) + " assignments"  + " and the error messages were: \n" , byAssigment)
