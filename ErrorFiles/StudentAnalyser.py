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
for assignment_id in query_result['assignment_id'].unique():
    language = query_result.loc[query_result['assignment_id'] == assignment_id].drop(['assignment_id','compile_errors'],
                                                                              axis=1).head(1).values.tolist()[0][0]
    files = query_result.loc[query_result['assignment_id'] == assignment_id].drop(['assignment_id', 'language'],
                                                                                  axis=1)
    #my_files = files
    my_files = files.values.tolist()
    my_bytes = Blob_File_Analysis.bytesToLines(my_files)
    if len(my_bytes) ==0:
        print("oops, dan maar niet")
    elif language == 1:
        print(haskell_parser(my_files))
    else:
        print(prolog_parser(my_files))

###
# 1e functie -> We geven student + oefz mee en we willen gewoon de opeenvolgende errors voor die oefz.
#
#
######

