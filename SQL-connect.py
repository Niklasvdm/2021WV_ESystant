import mysql.connector
import pandas as pd
from mysql.connector import Error
import Levenshtein


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
