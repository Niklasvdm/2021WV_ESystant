import TreeConstructor
import Queries
import Database_Functions



#host,root,passw = Database_Functions.NiklasConnectivity()
host, root, passw = Database_Functions.MaxConnectivity()


my_tree_query = Queries.getQuery03()
database = "esystant1920"
queryResult = Database_Functions.query_database_dataframe(host,root,passw,database,my_tree_query)
print(queryResult)

(datapoints,grades, categories,categoriesAndLanguages) = Database_Functions.groupByUserGradesAndCategories(queryResult)

#for x in datapoints:
#    print(x + ': ' + str(len(datapoints[x])))
#    print(datapoints[x][0])
(testDict,verificationDict) = TreeConstructor.splitBase(datapoints)

(categoryUsers,categoryGrades,splitCategories)  = TreeConstructor.prepareCategories(testDict,grades,categories,categoriesAndLanguages)


myDecisionTrees = TreeConstructor.buildTrees(categoryUsers,categoryGrades)


#   TODO:       HEEFT DE PLAATSING DE NULLEN EFFECT OP EINDRESULTAAT
# [0 for _ in range(len(list)]
#  Category = c
#
#
#
#
#
