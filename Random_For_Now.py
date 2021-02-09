from Database_Functions import create_database_connection
from Blob_File_Analysis import byteToLines, bytesToLines


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


"""
sql_prompt = '''
SELECT 
    opl_ID,
    category,
    SUM(nb_failed != 0) AS Failed_Submissions,
    SUM(nb_failed = 0) AS Successfulll_Submissions,
    SUM(r.style_result > '') AS amount_bad_style_submissions,
    SUM(s.points_awarded) AS Points,
    SUM(a.deadline * 10000 > s.timestamp) AS On_Time,
    SUM(a.deadline * 10000 < s.timestamp) AS Too_Late,
    score_prolog,
    score_haskell,
    u.user_id
FROM
    submissions AS s
        INNER JOIN
    results AS r ON r.submission_id = s.submission_id
        INNER JOIN
    assignments AS a ON a.assignment_id = s.assignment_id
        INNER JOIN
    users AS u ON u.user_id = s.user_id
        INNER JOIN
    grades AS g ON g.user_id = u.user_id
        INNER JOIN
    education_type AS e ON e.KULopl = u.KULopl
GROUP BY u.user_id , category
ORDER BY a.category ASC'''
"""