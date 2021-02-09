import mysql.connector
from mysql.connector import Error
from pandas import read_sql


def check_server_connectivity(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


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


def queryDatabase(query_text, database_name):
    my_cursor = create_database_connection("localhost", "root", "", database_name).cursor()
    my_cursor.execute(query_text)
    return my_cursor.fetchall()


def queryDatabaseDF(localhost, root, password, database, query):
    db = create_database_connection(localhost, root, password, database)
    return read_sql(query, db)

# input: output from query having done a query or querydatabase function
# ouput: a dictionary sorted by used and all results that used has had.
# REQUIREMENT: QUERY MUST HAVE USER AS FIRST IN SELECT CLAUSE
def groupByUser(results_from_query):
    myUserBase = {}
    for entry in results_from_query:
        if entry[0] in myUserBase:
            templist = [entry[1:]]
            secondtemplist = myUserBase[entry[0]]
            newList = secondtemplist.append(templist)
            # myUserBase[entry[0]] =
        else:
            myUserBase[entry[0]] = [[entry[1:]]]

    return myUserBase

