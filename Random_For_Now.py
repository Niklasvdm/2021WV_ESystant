from Database_Functions import create_database_connection
from Blob_File_Analysis import byteToLines, bytesToLines
from collections import Counter


# TODO comments fixen of dingen deleten
# Functie krijgt query als input die ~~~~~~~~1 FILE ~~~~~~~~ ophaalt en die naar een rij van lijnen
# omzet. Kan ook makkelijk geprint worden met printLines


# We moeten onze databases dezelfde naam geven want bij mij is dat Esystant_19_20 en we zouden ook best
# eenzelfde passwoord gebruiken
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
