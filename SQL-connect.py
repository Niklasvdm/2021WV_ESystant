import mysql.connector
import pandas as pd
from mysql.connector import Error
#import Levenshtein
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

main_df = pd.read_sql(sql_prompt, db)
"""
zoiets zou handig zijn als we zouden groeperen per user
main_df = main_df.head()
.tail(len(main_df.index)*0.9)- int(len(main_df.index)*0.9))
"""


#print(main_df)

#print(main_df.info)

used_cat_df = pd.read_sql("SELECT t.category FROM(" + sql_prompt + ") as t GROUP BY category", db)

#print(used_cat_df)

clf = tree.DecisionTreeRegressor(max_depth=3)
clf_mega = tree.DecisionTreeRegressor(max_depth=3)

dict_of_category_trees = {}

main_df_no_user = main_df.drop(columns=["user_id"])
for x in used_cat_df["category"]:
    df_of_category = main_df_no_user.query("category ==" + str(x)).drop(columns=["category"])
    indicators = []
    scores = []
    for l in df_of_category.values.tolist():
        indicators.append(l[:-2])
        scores.append(l[-2:])
    dict_of_category_trees[x] = clf.fit(indicators, scores)

all_user_df = pd.read_sql("SELECT user_id FROM users", db)


def get_data_user(user_id):
    df_of_user = main_df[main_df["user_id"] == user_id].drop(columns=["user_id"])
    if not df_of_user.empty:
        oplID = df_of_user["opl_ID"].iloc[0]
        scores = [df_of_user["score_prolog"].iloc[0], df_of_user["score_haskell"].iloc[0]]
    else:
        oplID = 0
        scores = [0, 0]

    indicators_user = []

    for cat in df_of_user["category"]:
        df_of_category_and_user = df_of_user[df_of_user.category == cat].drop(columns=["category"])
        for l in df_of_category_and_user.values.tolist():
            pred = dict_of_category_trees[cat].predict([l[:-2]])[0]
            indicators_user.append([cat, pred[0], pred[1]])

    for cat in [x for x in set(used_cat_df["category"]) if x not in set(df_of_user["category"])]:
        pred = dict_of_category_trees[cat].predict([[oplID, 0, 0, 0, 0, 0, 0]])[0]
        indicators_user.append([cat, pred[0], pred[1]])
    indicators_user.sort()
    return [x for row in indicators_user for x in row[1:]], scores


#print(df3.to_string())
#MEGATREE
indicators_mega,scores_mega = [], []
for user in all_user_df["user_id"]:
    data = get_data_user(user)
    indicators_mega.append(data[0])
    scores_mega.append(data[1])
#print("INDICATORS MEGA" , indicators_mega)
megatree = clf_mega.fit(indicators_mega,scores_mega)

def predictor(user_id):
    data_user, actual_answer = get_data_user(user_id)
    #print("INDICATORS PREDICTOR MEGA", indicators_of_user)
    prediction_megatree = megatree.predict([data_user])
    return prediction_megatree, actual_answer


for x in all_user_df["user_id"]:
    print(predictor(x))
