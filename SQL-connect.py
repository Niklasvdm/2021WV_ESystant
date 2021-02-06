import mysql.connector
import pandas as pd
from mysql.connector import Error
import Levenshtein
from sklearn import tree


def create_server_connection(host_name, user_name, user_password, selected_database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            auth_plugin='mysql_native_password',
            database=selected_database
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


db = create_server_connection("localhost", "root", "passwordroot", "Esystant_19_20")

'''
my_cursor = db.cursor()

sql_prompt = "SELECT file FROM Esystant_19_20.submissions where submission_id = 83860;"

#Manier 1:
my_cursor.execute(sql_prompt)
result = my_cursor.fetchall()

#Manier 2
df = pd.read_sql(sql_prompt, db)

for x in result:
    st = "".join([chr(z) for z in x[0]])
    print(Levenshtein.distance('father(fabian,anton).\nfather(anton,bart).\nfather(anton,daan).\nfather(anton,elisa).'
                   '\n\nmother(celine,bart).\nmother(celine,daan).\n\nmother(celine,gerda).\nmother(gerda,hendrik).'
                   '\n\nsibling(X,Y) :-\n\tfather(V,X), father(V,Y),\n\tmother(M,X), mother(M,Y),\n\tX \\= Y.'
                   '\n\nancestor(X,Y) :- father(X,Y).\nancestor(X,Y) :-\n\tfather(Z,Y),\n\tancestor(X,Z).\n\n',st))
    print(st)



# print(df)
'''
sql_prompt = '''
SELECT 
    opl_ID,
    category,
    SUM(nb_failed != 0) AS Failed_Submissions,
    SUM(nb_failed = 0) AS Successfulll_Submissions,
    SUM(r.style_result > '') AS amount_bad_style_submissions,
    SUM(s.points_awarded) AS Points,
    SUM(a.deadline * 10000 > s.timestamp) AS On_Time,
    SUM(a.deadline * 10000 < s.timestamp) AS Too_Late,
    score_prolog,
    score_haskell,
    u.user_id
FROM
    submissions AS s
        INNER JOIN
    results AS r ON r.submission_id = s.submission_id
        INNER JOIN
    assignments AS a ON a.assignment_id = s.assignment_id
        INNER JOIN
    users AS u ON u.user_id = s.user_id
        INNER JOIN
    grades AS g ON g.user_id = u.user_id
        INNER JOIN
    education_type AS e ON e.KULopl = u.KULopl
GROUP BY u.user_id , category
ORDER BY a.category ASC'''

df1 = pd.read_sql(sql_prompt, db)

#print(df1)

#print(df1.to_string())

df2 = pd.read_sql("SELECT t.category FROM(" + sql_prompt + ") as t GROUP BY category", db)

#print(df2)

clf = tree.DecisionTreeRegressor(max_depth=4)
clf_mega = tree.DecisionTreeRegressor(max_depth=4)

dict_of_category_trees = {}

df1_no_user = df1.drop(columns=["user_id"])
for x in df2["category"]:
    df_of_category = df1_no_user.query("category ==" + str(x)).drop(columns=["category"])
    indicators = []
    scores = []
    for l in df_of_category.values.tolist():
        indicators.append(l[:-2])
        scores.append(l[-2:])
    dict_of_category_trees[x] = clf.fit(indicators, scores)

df3 = pd.read_sql("SELECT user_id FROM users", db)

#print(df3.to_string())
#MEGATREE
indicators_mega,scores_mega = [], []
for user in df3["user_id"]:
    df_of_user = df1[df1["user_id"] == user].drop(columns=["user_id"])
    for cat in df2["category"]:
        df_of_category_and_user = df_of_user[df_of_user.category == cat].drop(columns=["category"])
        for l in df_of_category_and_user.values.tolist():
            pred = dict_of_category_trees[cat].predict([l[:-2]])[0]
            indicators_mega.append([cat, pred[0], pred[1]])
            scores_mega.append(l[-2:])
#print("INDICATORS MEGA" , indicators_mega)
megatree = clf_mega.fit(indicators_mega,scores_mega)

def predictor(user_id):
    dataframe = df1[df1["user_id"] == user_id].drop(columns=["user_id"])
    indicators_of_user = []
    for category in dataframe['category']:
        dataframe_of_category_and_user = dataframe[dataframe.category == category].drop(columns=["category"])
        prediction = dict_of_category_trees[category].predict([dataframe_of_category_and_user.values.tolist()[0][:-2]])[0]
        actual_answer = dataframe_of_category_and_user.values.tolist()[0][-2:]
        indicators_of_user.append([category, prediction[0], prediction[1]])
    #print("INDICATORS PREDICTOR MEGA", indicators_of_user)
    prediction_megatree = megatree.predict(indicators_of_user)
    print(prediction_megatree, actual_answer)

predictor('00e4208b3d1ddbf679c2f77c1f2322cb')






