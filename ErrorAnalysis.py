import  Queries
import Database_Functions
import  Blob_File_Analysis
from ErrorFiles.PossibleErrorsProlog import *
from ErrorFiles.PossibleErrorsHaskell import *

def main1():
    myquery = Queries.getQuery06()
    (host,root,passw) = Database_Functions.NiklasConnectivity()
    result = Database_Functions.get_query_database(host,root,passw,"esystant1920",myquery)
    lines = Blob_File_Analysis.bytesToLines(result)
    #Blob_File_Analysis.printLines(lines)
    return(lines)
def main2():
    #left_most_importance = -53
    msg = getExampleErrorMessagesProlog03()
    error_message_dictionary = {}
    error_message_list = []
    for i in msg:
        str = i[-53:]
        if str[:2] != 'Sy':
            str = i[-36:]
            if str[0] == ':':
                str = i[-31:]
            elif str[:2] == " S":
                str = str[1:]
            elif i[:7] == "Warning":
                str = "Warning"
            elif str[1] == ':' and str[3] == ':':
                str = str[5:]
            elif str[1] == ':':
                str = str[3:]
            elif i[:9] == "Traceback" or i[:9] == "Singleton":
                str = i[:9]
            elif i[:5] == "ERROR":
                str = "Error, too complex to display"
            else:
                str = str


        error_message_list.append(str)
        print(str)

    return error_message_list

#
# Template.hs:5:5:
# Temmplate.
#
def main3():
    a = 0
    msg = main1()
    for i in msg:
        msg[a] = i[2:] #MOET DIT?
        i = i[2:]
        a += 1
        if len(i) != 0:
            i[0] = i[0][4:]
            if i[0][:18] == "The type signature":
                i = ["Type Signature"]
        print(i)







main3()


#####
# We need an analyser for error messages. In order to do this we'll need to make some assumptions.
#   We'll write one function to analyse haskell & one for prolog.
#       more Parsers incoming....
#
#


# We can do this by seperating them and then calling each function individually.
#
#def anaylser(.blob_files):
#   (haskell_blob_files,prolog_blob_files) = seperateBlobFiles(.blob_files)
#   analyseProlog(prolog_blob_files)
#   analyseHaskell(haskell_blob_files)


#####
#
#
#
#def prologParser(prolog_blob_files):






