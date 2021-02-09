import TreeConstructor
import Queries
from Database_Functions import groupByUserAndGrades,get_query_database,NiklasConnectivity,MaxConnectivity



#host,root,passw = NiklasConnectivity()
host, root, passw = MaxConnectivity()


my_tree_query = Queries.getQuery02()
database = "esystant1920"
queryResult = get_query_database(host,root,passw,database,my_tree_query)
(datapoints,grades) = groupByUserAndGrades(queryResult)
(testDict,verificationDict) = TreeConstructor.splitBase(datapoints)
(categoryUsers,categoryGrades)  = TreeConstructor.prepareCategories(testDict,grades)
myDecisionTrees = TreeConstructor.buildTrees(categoryUsers,categoryGrades)
print(categoryUsers)