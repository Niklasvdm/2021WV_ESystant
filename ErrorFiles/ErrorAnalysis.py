from parse import *
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import linalg
########################################################################################################################
#           THIS FILE SERVES THE PURPOSE OF PARSING THE ERROR MESSAGES OF HASKELL & PROLOG
########################################################################################################################
#   FUNCTIONS:
#
#       ~ prologParser
#
#               REQUIREMENT: QUERY OUTPUT WITH MULTIPLE BLOB FILE CONVERTED USING Blob_File_Analysis.bytesToLines()
#               INPUT: [ [PROLOG_OUTPUT_0],[PROLOG_OUTPUT_1],...,[PROLOG_OUTPUT_N] ]
#               OUTPUT: [ [ ERROR_MESSAGE_0_0 , ERROR_MESSAGE_0_1 , ... , ERROR_MESSAGE_0_M ] , ....
#               [ ERROR_MESSAGE_N_0 , ERROR_MESSAGE_N_1 , ... , ERROR_MESSAGE_N_K] ]
#
#       ~ haskellParser
#
#               REQUIREMENT: QUERY OUTPUT WITH MULTIPLE BLOB FILE CONVERTED USING Blob_File_Analysis.bytesToLines()
#               INPUT: [ [HASKELL_OUTPUT_0],[HASKELL_OUTPUT_1],...,[HASKELL_OUTPUT_N] ]
#               OUTPUT: [ [ ERROR_MESSAGE_0_0 , ERROR_MESSAGE_0_1 , ... , ERROR_MESSAGE_0_M ] , ....
#               [ ERROR_MESSAGE_N_0 , ERROR_MESSAGE_N_1 , ... , ERROR_MESSAGE_N_K] ]
#
########################################################################################################################


# We can do this by seperating them and then calling each function individually.
#
# def anaylser(.blob_files):
#   (haskell_blob_files,prolog_blob_files) = seperateBlobFiles(.blob_files)
#   analyseProlog(prolog_blob_files)
#   analyseHaskell(haskell_blob_files)


########################################################################################################################
#               WE WANT THIS FUNCTION TO TAKE PROLOG COMPILE_ERROR FILES AND CONVERT THEM TO AN ARRAY WITH EACH ERROR
#               BRIEFLY MENTIONED
# -> Transorm data by putting it into lines. Funtionality done with ( Blob_File_Analysis.bytesToLines() )
#
# ###
#   INPUT: [ [PROLOG_OUTPUT_0],[PROLOG_OUTPUT_1],...,[PROLOG_OUTPUT_N] ]
#   OUTPUT : [ [ ERROR_MESSAGE_0_0 , ERROR_MESSAGE_0_1 , ... , ERROR_MESSAGE_0_M ] , ....
#   [ ERROR_MESSAGE_N_0 , ERROR_MESSAGE_N_1 , ... , ERROR_MESSAGE_N_K] ]
#
#
def prolog_parser(msg):
    final_message = []
    for i in msg:
        if i == [bytes(b'')]:
            final_message.append(["Empty file"]) # todo je gebruikt i dan ook niet meer. Gewoon de elif if maken zou volgens mij genoeg zijn?
        else:
            sequence = []
            for j in i:
                j = str(j)

                # Syntax Error
                result = search("Syntax Error", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Syntax Error")

                # Trying to modify procedure.
                result = search("modify static", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Trying to modify static procedure")

                # Traceback.
                result = search("traceback", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Traceback error")

                # Type error.
                result = search("Type error", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Type Error")

                # Warning
                result = search("warning", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Warning")

            if len(sequence) == 0:
                final_message.append(["Unknown Error"])
            else:
                final_message.append(sequence)

    return final_message

#
#
#
#
def prolog_numerical_parser(msg):
    final_message = []
    for i in msg:
        errorlist = []
        if i == [bytes(b''),0]:
            final_message.append(['0'])
            #print("Empty file")
        else:
           # sequence = []
            j = i[0]
            j = str(j)

            # Syntax Error
            result = search("Syntax Error", j, case_sensitive=False)
            if result is not None:
                errorlist.append('1')
                #sequence.append("Syntax Error")

            # Trying to modify procedure.
            result = search("modify static", j, case_sensitive=False)
            if result is not None:
                errorlist.append('2')
                #sequence.append("Trying to modify static procedure")

            # Traceback.
            result = search("traceback", j, case_sensitive=False)
            if result is not None:
                errorlist.append('3')
                #sequence.append("Traceback error")

            # Type error.
            result = search("Type error", j, case_sensitive=False)
            if result is not None:
                errorlist.append('4')
                #sequence.append("Type Error")

            # Warning
            result = search("warning", j, case_sensitive=False)
            if result is not None:
                errorlist.append('5')
                #sequence.append("Warning")
            #print("nonempty file")

        if len(errorlist) != 0:
            final_message.append(errorlist)
        # Possible -> Unknown Error.
        else:
            final_message.append(['Z'])
            # final_message.append('J')

    return final_message


def document_tfid_parser(documents):
    # So we want to parse one single document

    # Het werkt niet met alle documenten
    # vectorizer = TfidfVectorizer()
    # X = vectorizer.fit_transform(documents)
    # print(vectorizer.get_feature_names())
    # print(vectorizer.get_params())
    # print(vectorizer.get_stop_words())
    # print(X)
    # print(X.shape)
    sumOfDocuments = []
    for document in documents:
        sumOfDocuments.append(str(document[0]).replace('_',' '))
        # if len(document[0]) > 4:
        #     vectoriser = TfidfVectorizer()
        #     X = vectoriser.fit_transform(document)
        #     print(vectoriser.get_feature_names())
        #     print(vectoriser.get_params())
        #     print(vectoriser.get_stop_words())
        #     print(X.shape)
        #     print(X)
        # else:
        #     pass
    if len(sumOfDocuments) > 4:
        vectoriser = TfidfVectorizer(max_df=0.7)
        X = vectoriser.fit_transform(sumOfDocuments)
        print(vectoriser.get_feature_names())
        print(vectoriser.get_params())
        print(vectoriser.get_stop_words())
        print(X.shape)
        print(X)
    else:
        pass


########################################################################################################################
#               WE WANT THIS FUNCTION TO TAKE HASKELL COMPILE_ERROR FILES AND CONVERT THEM TO AN ARRAY WITH EACH ERROR
#               BRIEFLY MENTIONED
# -> Transorm data by putting it into lines. Funtionality done with ( Blob_File_Analysis.bytesToLines() )
#
# ###
#   INPUT: [ [HASKELL_OUTPUT_0],[HASKELL_OUTPUT_1],...,[HASKELL_OUTPUT_N] ]
#   OUTPUT : [ [ ERROR_MESSAGE_0_0 , ERROR_MESSAGE_0_1 , ... , ERROR_MESSAGE_0_M ] , ....
#   [ ERROR_MESSAGE_N_0 , ERROR_MESSAGE_N_1 , ... , ERROR_MESSAGE_N_K] ]
#
#
def haskell_parser(msg):
    final_message = []
    for i in msg:
        #i = i[2:]
        if i == [bytes(b'')]:
            print("Empty file")
            None # todo je gebruikt i dan ook niet meer. Gewoon de elif if maken zou volgens mij genoeg zijn?
        elif len(i) != 0:
            sequence = []
            for j in i:
                j = str(j)
                # The Type Signature was wrong
                result = search("The type signature", j, case_sensitive=False)
                if result is not None:
                    sequence.append("The Type Signature was wrong")

                # Variable not in scope
                result = search("Not in scope", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Variable not in scope")

                # Expected type not met
                result = search("expected type", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Expected type not met")

                # Problem with argument(s)
                result = search("argument", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Problem with argument(s)")

                # Function not in scope
                result = search("Not in scope", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Function not in scope")

                # Function is not the correct type
                result = search("Derived Instance", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Function is not the correct type")

                # Parse error occured
                result = search("parse", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Parse error occured")

                # Instance error
                result = search("instance", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Instance error")

                # Function missing
                result = search("No explicit implementation", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Function missing")

                # Multiple Declarations
                result = search("Multiple Declarations", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Multiple Declarations")

                # Syntax Error
                result = search("Syntax error", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Syntax Error")

                # Pattern Binding error
                result = search("Pattern binding", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Pattern Binding error")

                # Conflicting definitions
                result = search("conflicting definitions", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Conflicting definitions")

                # Module not loaded in
                result = search("find module", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Module not loaded in")

                # Error with pattern matching
                result = search("pattern match", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Error with pattern matching")

                # Lexical Error
                result = search("lexical error", j, case_sensitive=False)
                if result is not None:
                    sequence.append("Lexical Error")

                # operator Error
                result = search("operator", j, case_sensitive=False)
                if result is not None:
                    sequence.append("operator Error")

                # File name Error
                result = search("File name", j, case_sensitive=False)
                if result is not None:
                    sequence.append("File name Error")

            if len(sequence) != 0:
                final_message.append(sequence)
            # Possible -> Unknown Error.
            else:
                final_message.append(["Unknown Error"])
    return final_message

def haskell_numerical_parser(msg):
    final_message = []
    for i in msg:
        errorlist = []
        #i = i[2:]
        if i == [bytes(b''),0]:
           # print("Empty file")
            final_message.append(['0'])
            #None # todo je gebruikt i dan ook niet meer. Gewoon de elif if maken zou volgens mij genoeg zijn?
        elif len(i) != 0:
            j = i[0]
            j = str(j)
            # The Type Signature was wrong
            result = search("The type signature", j, case_sensitive=False)
            if result is not None:
                errorlist.append('1')
                #sequence.append("The Type Signature was wrong")

            # Variable not in scope
            result = search("Not in scope", j, case_sensitive=False)
            if result is not None:
                errorlist.append('2')
                #sequence.append("Variable not in scope")

            # Expected type not met
            result = search("expected type", j, case_sensitive=False)
            if result is not None:
                errorlist.append('3')
                #sequence.append("Expected type not met")

            # Problem with argument(s)
            result = search("argument", j, case_sensitive=False)
            if result is not None:
                errorlist.append('4')
                #sequence.append("Problem with argument(s)")

            # Function not in scope
            result = search("Not in scope", j, case_sensitive=False)
            if result is not None:
                errorlist.append('5')
                #sequence.append("Function not in scope")

            # Function is not the correct type
            result = search("Derived Instance", j, case_sensitive=False)
            if result is not None:
                errorlist.append('6')
                #sequence.append("Function is not the correct type")

            # Parse error occured
            result = search("parse", j, case_sensitive=False)
            if result is not None:
                errorlist.append('7')
                #sequence.append("Parse error occured")

            # Instance error
            result = search("instance", j, case_sensitive=False)
            if result is not None:
                errorlist.append('8')
                #sequence.append("Instance error")

            # Function missing
            result = search("No explicit implementation", j, case_sensitive=False)
            if result is not None:
                errorlist.append('9')
                #sequence.append("Function missing")

            # Multiple Declarations
            result = search("Multiple Declarations", j, case_sensitive=False)
            if result is not None:
                errorlist.append('A')
                #sequence.append("Multiple Declarations")

            # Syntax Error
            result = search("Syntax error", j, case_sensitive=False)
            if result is not None:
                errorlist.append('B')
                #sequence.append("Syntax Error")

            # Pattern Binding error
            result = search("Pattern binding", j, case_sensitive=False)
            if result is not None:
                errorlist.append('C')
                #sequence.append("Pattern Binding error")

            # Conflicting definitions
            result = search("conflicting definitions", j, case_sensitive=False)
            if result is not None:
                errorlist.append('D')
                #sequence.append("Conflicting definitions")

            # Module not loaded in
            result = search("find module", j, case_sensitive=False)
            if result is not None:
                errorlist.append('E')
                #sequence.append("Module not loaded in")

            # Error with pattern matching
            result = search("pattern match", j, case_sensitive=False)
            if result is not None:
                errorlist.append('F')
                #sequence.append("Error with pattern matching")

            # Lexical Error
            result = search("lexical error", j, case_sensitive=False)
            if result is not None:
                errorlist.append('G')
                #sequence.append("Lexical Error")

            # operator Error
            result = search("operator", j, case_sensitive=False)
            if result is not None:
                errorlist.append('H')
                #sequence.append("operator Error")

            # File name Error
            result = search("File name", j, case_sensitive=False)
            if result is not None:
                errorlist.append('I')
                #sequence.append("File name Error")
          #  print("nonempty file")

        if len(errorlist) != 0:
            final_message.append(errorlist)
        # Possible -> Unknown Error.
        else:
            final_message.append(['Z'])
            #final_message.append('J')
    return final_message