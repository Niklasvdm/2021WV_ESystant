import mysql.connector
from mysql.connector import Error
from pandas import read_sql


####################
# FILE FOR CHECKING DATABASE CONNECTIVITY, EXECUTING QUERIES, RETRIEVING BLOB FILES
#   Authors: Niklas Van der Mersch, Max Wübbenhorst
#
#
#
#
#######################
#   FUNCTIONS:
#
#       ~ NiklasConnectivity
#               INPUT : /
#               OUTPUT : NAME , ROOT , PASSWORD (x NIKLAS)
#
#
#       ~ MaxConnectivity =========================================== TODO =================
#               INPUT : /
#               OUTPUT : NAME , ROOT , PASSWORD (x MAX)
#
#
#
#       ~  check_server_connectivity. Prints if connections fails / succeeds.

#               INPUT: HOST_NAME , USER_NAME , USER_PASSWORD
#               OUTPUT : /
#
#       ~  create_database_connection
#
#               INPUT : HOST_NAME , USER_NAME , USER_PASSWORD , DATABASE
#               OUTPUT: CONNECTION TO SAID DATABASE IS SUCCESSFULL, NULL OTHERWISE.
#
#       ~  query_database
#
#               INPUT: HOST_NAME , USER_NAME , USER_PASSWORD , DATABASE , QUERY
#               OUTPUT: EXECUTED QUERY
#
#       ~  get_query_database
#
#               INPUT: HOST_NAME , USER_NAME , USER_PASSWORD , DATABASE , QUERY
#               OUTPUT: EXECUTED QUERY WITH FETCHALL
#
#       ~ groupByUser
#
#               REQUIREMENT: QUERY OUTPUT WITH USER IN FIRTST COLUMN
#               INPUT : QUERY OUTPUT [(USER_ID_0,PROPERTY_0_0,PROPERTY_0_1_...);(USER_ID_1,PROPERTY_1_0,PROPERTY_1_1_...);...;(USER_ID_N,PROPERTY_N_0,PROPERTY_N_1_...)]
#               OUTPUT : {( USER_ID_i : [[PROPERTY_i_0,PROPERTY_i_1,...],[PROPERTY_i_0,PROPERTY_i_1,...]) , ( USER_ID_(i+1) : [[PROPERTY_(i+1)_0,PROPERTY_(i+1)_1,...],
#                               [PROPERTY_(i+1)_0,PROPERTY_(i+1)_1,...]) , ... }
#                       Dictionary met users (key) en eigenschappen (property = value). Aangezien we veronderstellen dat 1 user meerdere rijen kan hebben,
#                               is de value een 2-D lijst.
#
#       ~ groupByUserAndGrades
#
#               REQUIREMENT: QUERY OUTPUT WITH USER IN FIRTST COLUMN AND GRADES IN THE LAST TWO COLUMNS
#               INPUT : QUERY OUTPUT [(USER_ID_0,PROPERTY_0_0,PROPERTY_0_1_...);(USER_ID_1,PROPERTY_1_0,PROPERTY_1_1_...);...;(USER_ID_N,PROPERTY_N_0,PROPERTY_N_1_...)]
#               OUTPUT : {( USER_ID_i : [[PROPERTY_i_0,PROPERTY_i_1,...],[PROPERTY_i_0,PROPERTY_i_1,...]) , ... } ,
#                           {( USER_ID_i : [GRADE_i_01,GRADE_i_02) , ( USER_ID_j : [GRADE_j_01,GRADE_j_02) ,... }
#                       Dictionary met users (key) en eigenschappen (property = value). Aangezien we veronderstellen dat 1 user meerdere rijen kan hebben,
#                               is de value een 2-D lijst.
#
#
#####################

def NiklasConnectivity():
    return (niklashost, niklasroot, niklaspassw)


niklashost = "localhost"
niklasroot = "root"
niklaspassw = ""

def MaxConnectivity():
    return (maxhost, maxroot, maxpassw)

maxhost = "localhost"
maxroot = "root"
maxpassw = "passwordroot"


def check_server_connectivity(host_name, user_name, user_password):
    try:
        mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return


def create_database_connection(host_name, user_name, user_password, selected_database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            database=selected_database,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection to", selected_database, "successfull")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def query_database_dataframe(localhost, root, password, database, query):
    db = create_database_connection(localhost, root, password, database)
    return read_sql(query, db)

def get_query_database(localhost, root, password, database_name, query_text):
    db = create_database_connection(localhost, root, password, database_name)
    my_cursor = db.cursor()
    my_cursor.execute(query_text)
    result = my_cursor.fetchall()
    return result


# REQUIREMENT: QUERY MUST HAVE USER AS FIRST IN SELECT CLAUSE
# input: output from query having done a query or querydatabase function
# ouput: a dictionary sorted by used and all results that used has had.
def groupByUser(results_from_query):
    myUserBase = {}
    for entry in results_from_query:
        if entry[0] in myUserBase:
            templist = list(entry[1:])
            secondtemplist = myUserBase[entry[0]]
            secondtemplist.append(templist)
        else:
            myUserBase[entry[0]] = [list(entry[1:])]

    return myUserBase


# # REQUIREMENT: QUERY MUST HAVE USER AS FIRST IN SELECT CLAUSE AND PROLOG & HASKELL SCORE AS LAST TWO COLUMNS
# input: output from a query or querydatabase function
# ouput: a dictionary sorted by user and all results (CATEGORIES) that user has had.
def groupByUserAndGrades(results_from_query):
    dataUserBase = {}
    gradesUserBase = {}
    for entry in results_from_query:
        if entry[0] in dataUserBase:
            templist = list(entry[1:-2])
            secondtemplist = dataUserBase[entry[0]]
            secondtemplist.append(templist)
        else:
            dataUserBase[entry[0]] = [list(entry[1:-2])]
            gradesUserBase[entry[0]] = list(entry[-2:])

    return (dataUserBase, gradesUserBase)

# # REQUIREMENT: QUERY MUST HAVE USER AS FIRST IN SELECT CLAUSE AND PROLOG & HASKELL SCORE AS LAST TWO COLUMNS
# input: output from a query or querydatabase function
# ouput: a dictionary sorted by user and all results (CATEGORIES) that user has had.
#
# TODO: Documentation
#
def groupByUserGradesAndCategories(results_from_query):
    dataUserBase = {}
    gradesUserBase = {}
    allcategories = set()
    allcategoriesWithLanguage = set()
    #for entry in results_from_query:
    for entry in results_from_query.values.tolist():
        allcategories.add(entry[1])
        allcategoriesWithLanguage.add((entry[1],entry[-3]))
        if entry[0] in dataUserBase:
            templist = list(entry[1:-2])
            secondtemplist = dataUserBase[entry[0]]
            secondtemplist.append(templist)
        else:
            dataUserBase[entry[0]] = [list(entry[1:-2])]
            gradesUserBase[entry[0]] = list(entry[-2:])

    return (dataUserBase, gradesUserBase,allcategories,allcategoriesWithLanguage)


