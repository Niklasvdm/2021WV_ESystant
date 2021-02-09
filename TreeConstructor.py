from Database_Functions import NiklasConnectivity,create_database_connection
from random import shuffle
from Database_Functions import groupByUserAndGrades,groupByUser,get_query_database,NiklasConnectivity,MaxConnectivity
from sklearn import tree
import Queries



######## FUNCTIONS:
#
#   ~ splitBase
#
#           INPUT: Dictionary
#           OUTPUT: (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
#

# First thing we're going to do is just writing a function to fetch data. We write two: One given just a query and a
# database,  one more detailed with host info

# Ook in deze file weer belangrijk dat we de naam van databases en passwoord matchen
# Er is een 2e functie voor die reden.

# https://stackoverflow.com/questions/12988351/split-a-dictionary-in-half
# INPUT: DICTIONARY
# OUTPUT: TUPLE (DICTIONARY_TEST,DICTIONARY_VERIFICATION)
#       Function takes the dictionary and shuffles it randomly to produce shuffled result.
def splitBase(d):
    temp = (list(d.items()))
    shuffle(temp)
    return ( dict(temp[:int(len(d) * TEST_PERCENTAGE)]) , dict(temp[int(len(d) * TEST_PERCENTAGE):]) )


TEST_PERCENTAGE = 0.9
VERIFICATION_PERCENTAGE = 1 - TEST_PERCENTAGE


##################################################
# Nu willen we gewoon een functie kunnen geven dat een query ( en de nodige informatie neemt als input) en het resultaat van de decision tree meegeeft.
#   Dit wordt eventueel gedaan met verschillende hulpfuncties.
#       Om dit te doen werken : 1e kolom user id, 2e kolom per oefenzitting , laatste 2 kolommen Prolog & Haskell Respectively.
###################################################






#
# input: dictionary van per user verschillende arrays met eigenschappen. Dit in een dictionary
# output: Per categorie een boom op de overblijvende eigenschapper per user.
# {USER:[[CATEGORY_0,_],[CATEGORY_1,_],...]}
# CATEGORY_0 X [PROPERTY_0,PROPERTY_1,...] -> DECISION TREE_0 , CATEGORY_1 X [PROPERTY_0,PROPERTY_1,...] -> DECISION TREE_0
#
#   For each category we want to build a tree. This is done with preparecategories and buildTrees
#
# NEXT: BUILD MEGATREE
#       INPUT:
#       OUTPUT:
#
#



# Function that per Category, makes a dictionary with all of the user necessairy and a list with the necessairy grades
#       REQUIREMENT: EERSTE PLAATS IN DICTIONARY USER IS CATEGORIE,LAATSTE PLAATS IS TAAL.
#                       GRADESDICTIONARY KOMT OVEREEN MET [PUNT_PROLOG,PUNT_HASKELL]
#       INPUT : { USER : [[CAT_0,...,LANGUAGE],[CAT_1,...,LANGUAGE],...]) , .... }
#               { USER : [GRADE_PROLOG,GRADE_HASKELL],... }
#       OUTPUT : { ( CATEGORY_0 : [ [PROPERTY_0,PROPERTY_1,....],[PROPERTY_0,PROPERTY_1,...] ] ) , ( ...) , ....}
#                { ( CATEGORY_0 : [ GRADE_0_0,GRADE_0_1,...] ) , ( CATEGORY_1 : [ GRADE_1_0,GRADE_1_1,...] ) , ... }
#
#
def prepareCategories(testDictionary,gradesDictionary):
    exercizeDictionary = {}
    exercizeGradeDictionary = {}
    category_sets = [set(),set()]
    for users in testDictionary: # ELKE USER HEEFT [[CAT_0,...,LANGUAGE],[CAT_1,...,LANGUAGE],...]
        for user_list in testDictionary[users]:
            language = user_list[-1] % 2  # 1 voor haskell, 0 voor Prolog.
            category_sets[language].add(user_list[0])
            if user_list[0] in exercizeDictionary:
                exercizeDictionary[user_list[0]].append(user_list[1:-1])
                gradeStudent = gradesDictionary[users][language]
                exercizeGradeDictionary[user_list[0]].append(gradeStudent)
            else:
                exercizeDictionary[user_list[0]] = [user_list[1:-1]] #Neem eerst alle nuttige informatie.
                gradeStudent = gradesDictionary[users][language] # Neem de grade van de student.
                exercizeGradeDictionary[user_list[0]] = [gradeStudent] #Stop die in de lijst.
    return(exercizeDictionary,exercizeGradeDictionary)

# DOEL VAN BUILDTREES: we bouwen een boom per categorie met de nodige punten
#   INPUT: { CATEGORY_0 : [ LIST_0_0 , LIST_0_1 , ... LIST_0,N0] , CATEGORY_1 : [ LIST_1_0 , LIST_1_1 , ... LIST_1,N1]  , .... }
#          { CATEGORY_0 : [ GRADE_0_0 , GRADE_0_1 , ... GRADE_0,N0] , CATEGORY_1 : [ GRADE_1_0 , GRADE_1_1 , ... GRADE_1,N1]  , .... }
#   OUTPUT: { CATEGORY_0 : DECISION_TREE_0  , CATEGORY_1 : DECISION_TREE_1  , ... }
def buildTrees(DictionaryCategories,DictionaryGrades):
    decisionTrees = {}
    for category in DictionaryCategories:
        clf = tree.DecisionTreeRegressor()
        listValues = DictionaryCategories[category]
        listGrades = DictionaryGrades[category]
        decisionTrees[category] = clf.fit(listValues,listGrades)
    return decisionTrees

# PURPOSE: Build megatree
#
#
#
def buildMegaTree(decisionTrees, DictionaryCategories,DictionaryGrades):
    clf = tree.DecisionTreeRegressor()

    #listValues = DictionaryCategories[category]
    #listGrades = DictionaryGrades[category]

    return




# DOEL VAN DEZE FUNCTIE: NAGAAN HOE GOED DE TREE IS.
#       INPUT:  { CATEGORY_0 : DECISION_TREE_0  , CATEGORY_1 : DECISION_TREE_1  , ... }
#               { USER : [[CAT_0,...,LANGUAGE],[CAT_1,...,LANGUAGE],...]) , .... }
#
#
#
#checkTrees(DictionaryTrees)


# limit = 25
# for i in testDict:
#     for j in testDict[i]:
#         for k in j:
#             print(k)
#             limit -= 1
#     if limit == 0:
#         break



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
