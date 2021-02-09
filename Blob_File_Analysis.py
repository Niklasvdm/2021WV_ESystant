# Idee van deze file: functies schrijven dat ervoor zorgt dat wij makkelijk BLOB files kunnen analyseren.
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
    # Waarom juist deze functie?

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

