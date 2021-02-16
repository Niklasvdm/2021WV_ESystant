import  Queries
import Database_Functions
import  Blob_File_Analysis
from ErrorFiles.PossibleErrorsProlog import *
from ErrorFiles.PossibleErrorsHaskell import *

def main1():
    myquery = Queries.getQuery04()
    (host,root,passw) = Database_Functions.NiklasConnectivity()
    result = Database_Functions.get_query_database(host,root,passw,"esystant1920",myquery)
    lines = Blob_File_Analysis.bytesToLines(result)
    Blob_File_Analysis.printLines(lines)

def main2():
    msg = getExampleErrorMessagesProlog01()
    error_message_dictionary = {}
    for i in msg:
        for j in i[-36:]:
            if j == ':':
                return


main1()


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






