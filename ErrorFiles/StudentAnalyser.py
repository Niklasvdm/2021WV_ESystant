import Database_Functions
from Queries import *
from ErrorAnalysis import *
import Blob_File_Analysis

host,root,passw = Database_Functions.NiklasConnectivity()
database1617 = "esystant1617"
database1718 = "esystant1718"
database1819 = "esystant1819"
database1920 = "esystant1920"
database = database1920

myQuery = get_query_06()


query_result = Database_Functions.query_database_dataframe(host,root,passw,database,myQuery)
print(query_result)
for category in query_result['category'].unique():
    language = query_result.loc[query_result['category'] == category].drop(['category','compile_errors','assignment_id'],
                                                                              axis=1).head(1).values.tolist()[0][0]
    category_df = query_result.loc[query_result['category'] == category].drop(['category'],
                                                                              axis=1)
    byAssigment = []
    a= 0
    for assignment_id in category_df['assignment_id'].unique():
        files = category_df.loc[category_df['assignment_id'] == assignment_id].drop(['assignment_id', 'language'],
                                                                                      axis=1)

        my_files = files.values.tolist()
        if len(my_files) ==0:
            print("oops, dan maar niet")
        elif language == 1:
            byAssigment.append(haskell_parser(my_files))
        else:
            byAssigment.append(prolog_parser(my_files))
        a += 1
    print("the category was: " + str(category) + " there were " + str(a) + " assignments"  + " and the error message was: \n" , byAssigment)

###
# 1e functie -> We geven student + oefz mee en we willen gewoon de opeenvolgende errors voor die oefz.
#
#
######

