import mysql.connector
from mysql.connector import Error
import pandas as pd


#Idee van deze file: functies schrijven dat ervoor zorgt dat wij makkelijk BLOB files kunnen analyseren.
#
#   FUNCTIES:
#       CHECK_SERVER_CONNECTION
#       CREATE_DATABASE_CONNECTION
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
#      DATABASETOLINES
#           databaseToLines(localhost,root,password,database,query)
#               ~Vrij vanzelfssprekend.
#
#
#
#
#


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
            database = 'esystant1920',
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection to", selected_database , "successfull")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def byteToOutput(mybytes):
    #lines = []
    mystr = ''
    for i in str(mybytes)[4:]:
        mystr += i
        lastletters = mystr[-2:]
        if lastletters == '\\n':
            print(mystr[:-2])
            #lines.append(mystr[:-2])
            mystr = ''
        elif lastletters == '\\t':
            #print(' ' + mystr[:-2])
            mystr = '   ' + mystr[:-2]
        elif lastletters == '\\':
            mystr = mystr[-1]

def byteToLines(mybytes):
    lines = []
    mystr = ''
    for i in str(mybytes)[4:]:
        mystr += i
        lastletters = mystr[-2:]
        if lastletters == '\\n':
            #print(mystr[:-2])
            lines.append(mystr[:-2])
            mystr = ''
        elif lastletters == '\\t':
            #print(' ' + mystr[:-2])
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
            #print(mystr[:-2])
            lines.append(mystr[:-2])
            mystr = ''
        elif lastletters == '\\t':
            #print(' ' + mystr[:-2])
            mystr = '   ' + mystr[:-2]
        elif lastletters == '\\':
            mystr = mystr[-1:]

        if mystr == '",), (b"':
            multiplelines.append(lines)
            lines = []
            mystr = ''
    return multiplelines

#Functie dat u lines gewoon print
def printlines(lines):
    for i in lines:
        print(i)

def printMultipleLines(lines):
    for i in lines:
        for j in i:
            print(j)


# Functie krijgt query als input die ~~~~~~~~1 FILE ~~~~~~~~ ophaalt en die naar een rij van lijnen
# omzet. Kan ook makkelijk geprint worden met printLines
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


#sql_prompt = "SELECT compile_errors FROM results where result_id BETWEEN 41309 AND 41312 ;"

#printMultipleLines(queryMultipleResultsToLines(sql_prompt))

def databaseToLines(localhost,root,password,database,query):
    db = create_database_connection(localhost,root,password,database)
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return bytesToLines(result)



