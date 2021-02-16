from Database_Functions import create_database_connection

#### PURPOSE:
#           THIS FILE SERVES THE PURPOSE OF ANALYSING BLOB FILES.
#           THIS INCLUDES READING THE BLOB FILES AND CLEANING IT INTO READABLE PIECS
#
#
#
#
#
##################### FUNCTIONS:
#
#       ~ byteToLines
#
#               REQUIREMENT: QUERY OUTPUT WITH SINGLE BLOB FILE
#               INPUT: BYTE FROM DATABASE CURSOR.
#               OUTPUT: 1-D LIST WITH BLOB FILE OUTPUT
#
#       ~ databaseToLine
#
#               REQUIREMENT: QUERY OUTPUT WITH SINGLE BLOB FILE
#               INPUT: HOST_NAME , USER_NAME , USER_PASSWORD , DATABASE , QUERY
#               OUTPUT: 1-D LIST WITH OUTPUT BLOB FILE
#
#       ~ printLine
#
#               INPUT: line from byteToLines() function
#               OUTPUT: /
#
#       ~ bytesToLines
#
#               REQUIREMENT: QUERY OUTPUT WITH MULTIPLE BLOB FILES
#               INPUT: BYTES FROM DATABASE CURSOR.
#               OUTPUT: 2-D LIST WITH EACHT LIST EACH ELEMENT A LINE OF THE BLOB FILE
#
#       ~ databaseToLines
#
#               REQUIREMENT: QUERY OUTPUT WITH MULTIPLE BLOB FILES
#               INPUT: HOST_NAME , USER_NAME , USER_PASSWORD , DATABASE , QUERY
#               OUTPUT: 2-D LIST WITH EACHT LIST EACH ELEMENT A LINE OF THE BLOB FILE
#
#       ~ printLines
#
#               INPUT: lines from bytesToLines() function
#               OUTPUT: /
###############################################################




#       BYTETOLINES:
# INPUT: BYTE FROM SINGLE BLOB FILES
# OUTPUT: [STRING]
#
def byteToLines(mybytes):
    # doet hetzelfde als "".join([chr(z) for z in mybytes[0]]).replace('\t','   ').split('\n')
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


#       DATABASETOLINE
# INPUT: DATABASE CONNECTIVITY THAT HAS OUTPUT SINGLE BLOB FILES
# OUTPUT [STRING]
def databaseToLine(localhost, root, password, database, query):
    db = create_database_connection(localhost, root, password, database)
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return byteToLines(result)


# Functie dat u lines gewoon print
def printLine(lines):
    for i in lines:
        print(i)


#       BYTESTOLINES:
# INPUT: BYTE FROM MULTIPLE BLOB FILES
# OUTPUT: [[STRING]]
#
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

        if mystr == '",), (b"' or mystr == """",), (b'""" or mystr == """',), (b'""" or mystr == '''',), (b"''' or mystr == "',), (b'":
            multiplelines.append(lines)
            lines = []
            mystr = ''

        if len(mystr) > 8:
            if mystr[-8:] == '",), (b"' or mystr[-8:] == """",), (b'""" or mystr[-8:] == """',), (b'""" or mystr[-8:] == '''',), (b"''' or mystr[-8:] == "',), (b'":
                multiplelines.append(lines)
                lines = []
                mystr = ''

    return multiplelines


#       BYTESTOLINES:
# INPUT: BYTE FROM MULTIPLE BLOB FILES
# OUTPUT: [[STRING]]
#
def bytesToLines_(mybytes):
    multiplelines = []
    lines = []
    mystr = ''
    for i in mybytes:
        print(i)

    return multiplelines

#       DATABASETOLINES
# INPUT: DATABASE CONNECTIVITY THAT HAS OUTPUT MULTIPLTE BLOB FILES
# OUTPUT [[STRING]]
def databaseToLines(localhost, root, password, database, query):
    db = create_database_connection(localhost, root, password, database)
    my_cursor = db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return bytesToLines(result)


# Equivalente functie voor multiple lines
def printLines(lines):
    for i in lines:
        for j in i:
            print(j)







