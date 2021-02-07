from BlobFileAnalysis import create_database_connection


# POSSIBLE FUNCTIONS IN THIS FILE ARE:
#
# QUERYDATABASE
#       INPUT: query,database from which it comes. Returns normal results as seen in esystant
#       OUTPUT: result from that query
# QUERY
#       INPUT: localhost,root,password,database,query
# GROUPBYUSER
#       INPUT: output from one of the afformentioned query functions
#       OUTPUT: dictionary with per user, all of the data in a 2-D array. (so per user)
# TESTBASE
#       INPUT: Output from groupybyuser() call
#       OUTPUT: the first TEST_PERCENTAGE Of the users and their respective information. (set to 0.9 normally)
# VERIFICATIONBASE
#       INPUT; Same as above
#       OUTPUT: the other TEST_PERCENTAGE of the users.
#
#

# First thing we're going to do is just writing a function to fetch data. We write two: One given just a query and a
# database,  one more detailed with host info

# Ook in deze file weer belangrijk dat we de naam van databases en passwoord matchen
def queryDatabase(query_text, database_name):
    db = create_database_connection("localhost", "root", "", database_name)
    my_cursor = db.cursor()
    my_cursor.execute(query_text)
    result = my_cursor.fetchall()
    return result


def query(localhost, root, password, database_name, query_text):
    db = create_database_connection(localhost, root, password, database_name)
    my_cursor = db.cursor()
    my_cursor.execute(query_text)
    result = my_cursor.fetchall()
    return result


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


# https://stackoverflow.com/questions/12988351/split-a-dictionary-in-half
# Easy function. Just takes the first 90% Of the users.
# For easy measure, change variable TEST_PERCENTAGE
def testBase(d):
    return dict(list(d.items())[:int(len(d) * TEST_PERCENTAGE)])


def verificationBase(d):
    return dict(list(d.items())[int(len(d) * TEST_PERCENTAGE):])


TEST_PERCENTAGE = 0.9
VERIFICATION_PERCENTAGE = 1 - TEST_PERCENTAGE

my_query = "SELECT DISTINCT user_id, assignment_id FROM submissions " \
           "WHERE user_id = '00e4208b3d1ddbf679c2f77c1f2322cb' ORDER BY user_id ASC"
database = "esystant1920"
queryResult = queryDatabase(my_query, database)
byUser = groupByUser(queryResult)
testDict = testBase(byUser)
verificationDict = verificationBase(byUser)

# clf = tree.DecisionTreeRegressor(max_depth=4)
#
# prologSessions1920 = pd.read_csv("Project SlayTheDragon\Datafiles\PrologSessions1920.csv")
#
# # Splits op zodat amount of submissions opgesplitst is per oefenzitting.
#
# session01, session02, session03, session04, sessionindividual = [], [], [], [], []
# score01, score02, score03, score04, scoreIndividual = [], [], [], [], []
#
# # Per student zal er dus 1 element zijn: Het aantal submissions.
# for x in range(int(len(prologSessions1920['user_id']) * 0.9)):
#     if prologSessions1920['category'][x] == 8:
#         session01.append([prologSessions1920['Submission_Amount'][x]])
#         score01.append([prologSessions1920['score_prolog'][x]])
#     elif prologSessions1920['category'][x] == 9:
#         session02.append([prologSessions1920['Submission_Amount'][x]])
#         score02.append([prologSessions1920['score_prolog'][x]])
#     elif prologSessions1920['category'][x] == 10:
#         session03.append([prologSessions1920['Submission_Amount'][x]])
#         score03.append([prologSessions1920['score_prolog'][x]])
#     elif prologSessions1920['category'][x] == 12:
#         session04.append([prologSessions1920['Submission_Amount'][x]])
#         score04.append([prologSessions1920['score_prolog'][x]])
#     else:
#         sessionindividual.append([prologSessions1920['Submission_Amount'][x]])
#         scoreIndividual.append([prologSessions1920['score_prolog'][x]])
#
# treeSession01 = clf.fit(session01, score01)
# treeSession02 = clf.fit(session02, score02)
# treeSession03 = clf.fit(session03, score03)
# treeSession04 = clf.fit(session04, score04)
# # treeSessionIndividual = clf.fit(sessionindividual,scoreIndividual)
#
#
# # Building the BIG Tree
#
# # Nu hebben we de bomen, nu willen we zorgen dat we effectief iets kunnen voorspellen?
#
# correct = 0
# incorrect = 0
#
# for x in range(int(len(prologSessions1920['user_id']) * 0.9), len(prologSessions1920['user_id'])):
#     if prologSessions1920['category'][x] == 8:
#         pred = treeSession01.predict(prologSessions1920['Submission_Amount'][x])
#     elif prologSessions1920['category'][x] == 9:
#         pred = treeSession02.predict(prologSessions1920['Submission_Amount'][x])
#     elif prologSessions1920['category'][x] == 10:
#         pred = treeSession03.predict(prologSessions1920['Submission_Amount'][x])
#     elif prologSessions1920['category'][x] == 12:
#         pred = treeSession04.predict(prologSessions1920['Submission_Amount'][x])
#     else:
#         pred = treeSessionIndividual.predict([prologSessions1920['Submission_Amount'][x]])[0]
#
#     score = prologSessions1920['score_prolog'][x]
#     print(pred, score)
#     if ((pred <= 5 and score > 5) or (pred > 5 and score <= 5)):
#         incorrect += 1
#     else:
#         correct += 1
# print(correct, incorrect)
