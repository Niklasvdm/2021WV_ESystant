import TreeConstructor
import Queries
import Database_Functions



#host,root,passw = Database_Functions.NiklasConnectivity()
host, root, passw = Database_Functions.MaxConnectivity()


my_tree_query = Queries.getQuery02()
database = "esystant1920"
queryResult = Database_Functions.get_query_database(host,root,passw,database,my_tree_query)
(datapoints,grades) = Database_Functions.groupByUserAndGrades(queryResult)
for x in datapoints:
    print(x + ': ' + str(len(datapoints[x])))
    print(datapoints[x][0])
(testDict,verificationDict) = TreeConstructor.splitBase(datapoints)
(categoryUsers,categoryGrades)  = TreeConstructor.prepareCategories(testDict,grades)
myDecisionTrees = TreeConstructor.buildTrees(categoryUsers,categoryGrades)
