import mysql.connector
from mysql.connector import Error


# Idee van deze file: functies schrijven dat ervoor zorgt dat wij makkelijk BLOB files kunnen analyseren.
#
#   FUNCTIES:
#       BYTETOOUTPUT
#              input = een cursos.fetchall operatie met 1 file
#               output = \ -> een print van die informatie geformateerd
#             is voor .blob file in te lezen en te printen
#       BYTETOLINES
#              idem, maar geeft een lijst terug met geformateerde lijnen van tekst.
#       BYTESTOLINES
#               Equivalent, maar multiple files kunnen nu ingelezen worden. Om te printen bestaat makkelijk
#               de functie printMultipleLines
#       PRINTLINES
#       PRINTMULTIPLELINES
#       QUERYTOLINES
#           input: query met 1 file als output
#           output : die geformateerde files in str in 1-D lijst
#       QUERYMULTIPLERESULTSTOLINES
#           input: query dat verschillende files als input neemt
#           ouput : Alle geformateerde strings in een 2-D lijst.
#      GETRESULTSFROMDATABASE
#      DATABASETOLINES
#           databaseToLines(localhost,root,password,database,query)
#               ~Vrij vanzelfssprekend.
#
#
#
#
#


def byteToOutput(mybytes):
    # doet hetzelfde als "".join([chr(z) for z in mybytes[0]])

    mystr = ''
    for i in str(mybytes)[3:-3]:
        mystr += i
        lastletters = mystr[-2:]
        if lastletters == '\\n':
            print(mystr[:-2])
            # lines.append(mystr[:-2])
            mystr = ''
        elif lastletters == '\\t':
            # print(' ' + mystr[:-2])
            mystr = '   ' + mystr[:-2]
        elif lastletters == '\\':
            mystr = mystr[-1]
    return mystr


def byteToLines(mybytes):
    # doet hetzelfde als "".join([chr(z) for z in mybytes[0]]).replace('\t','   ').split('\n')
    # Waarom is replace nodig?

    lines = []
    mystr = ''
    for i in str(mybytes)[3:-2]:
        mystr += i
        lastletters = mystr[-2:]
        if lastletters == '\\n':
            # print(mystr[:-2])
            lines.append(mystr[:-2])
            mystr = ''
        elif lastletters == '\\t':
            # print(' ' + mystr[:-2])
            mystr = '   ' + mystr[:-2]
        elif lastletters == '\\':
            mystr = mystr[-1]
    return lines


def bytesToLines(mybytes):

    multiplelines = []
    lines = []
    mystr = ''
    for i in str(mybytes)[4:]:
        mystr += i
        lastletters = mystr[-2:]
        if lastletters == '\\n':
            # print(mystr[:-2])
            lines.append(mystr[:-2])
            mystr = ''
        elif lastletters == '\\t':
            # print(' ' + mystr[:-2])
            mystr = '   ' + mystr[:-2]
        elif lastletters == '\\':
            mystr = mystr[-1:]

        if mystr == '",), (b"':
            multiplelines.append(lines)
            lines = []
            mystr = ''
    return multiplelines


# Functie dat u lines gewoon print
def printlines(lines):
    for i in lines:
        print(i)


def printMultipleLines(lines):
    for i in lines:
        for j in i:
            print(j)


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




# sql_prompt = "SELECT result_id,submission_id FROM results where result_id BETWEEN 41309 AND 41312 ;"
# printMultipleLines(queryMultipleResultsToLines(sql_prompt))
