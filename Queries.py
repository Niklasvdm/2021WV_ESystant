########################################################################################################################
# FILE TO CONVENIENTLY GROUP ALL QUERIES
#   Authors: Niklas Van der Mersch, Max Wübbenhorst
########################################################################################################################
#   FUNCTIONS:
#
#       ~ get_query_01
#           user_id, category, Failed_Submissions, Successful_Submissions, amount_bad_style_submissions, Points,
#           On_Time, Too_Late, score_prolog, score_haskell
#
#
#       ~ get_query_02
#           user_id, category, Failed_Submissions, Successful_Submissions, amount_bad_style_submissions, Points,
#           On_Time, Too_Late, language, score_prolog, score_haskell
#
#
#       ~ get_query_03
#           user_id, category, opl_ID, Failed_Submissions, Successful_Submissions, amount_bad_style_submissions, Points,
#           On_Time, Too_Late, language, score_prolog, score_haskell
#
#
#       ~ get_query_04
#          compile_errors of user 4bd1135791ab4afe4d9f3215ea1705f8
#
#
#       ~ get_query_05
#          user_id, category, opl_ID, Failed_Submissions, Successful_Submissions, amount_bad_style_submissions, Points,
#          On_Time, Too_Late, language, score_prolog, score_haskell
#          filtered on submissions before the exam
#
#
#       ~ get_query_06
#          compile_errors of user 0956c2c7071ae611c2f740e3685ed470
#
#
#       ~ get_query_07
#          compile_errors of user a706bb348b2a0c23e35ae11e4d68fc17 and language prolog
########################################################################################################################


def get_query_01():
    query = """SELECT 
        u.user_id,
        category,
        SUM(nb_failed != 0) AS Failed_Submissions,
        SUM(nb_failed = 0) AS Successful_Submissions,
        SUM(r.style_result > '') AS amount_bad_style_submissions,
        SUM(s.points_awarded) AS Points,
        SUM(a.deadline * 10000 > s.timestamp) AS On_Time,
        SUM(a.deadline * 10000 < s.timestamp) AS Too_Late,
        score_prolog,
        score_haskell
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
    GROUP BY user_id , category"""
    return query


def get_query_02():
    query = """
    SELECT 
        u.user_id,
        category,
        SUM(nb_failed != 0) AS Failed_Submissions,
        SUM(nb_failed = 0) AS Successful_Submissions,
        SUM(r.style_result > '') AS amount_bad_style_submissions,
        SUM(s.points_awarded) AS Points,
        SUM(a.deadline * 10000 > s.timestamp) AS On_Time,
        SUM(a.deadline * 10000 < s.timestamp) AS Too_Late,
        language,
        score_prolog,
        score_haskell
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
    GROUP BY user_id , category , language
    """
    return query


def get_query_03():
    query = """
    SELECT 
        u.user_id,
        category,
        opl_ID,
        SUM(nb_failed != 0) AS Failed_Submissions,
        SUM(nb_failed = 0) AS Successful_Submissions,
        SUM(r.style_result > '') AS amount_bad_style_submissions,
        SUM(s.points_awarded) AS Points,
        SUM(a.deadline * 10000 > s.timestamp) AS On_Time,
        SUM(a.deadline * 10000 < s.timestamp) AS Too_Late,
        language,
        score_prolog,
        score_haskell
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
GROUP BY u.user_id , category, language
ORDER BY a.category ASC
    """
    return query


def get_query_04():
    query = """
    SELECT r.compile_errors
    FROM results as r 
    INNER JOIN submissions as s on s.submission_id = r.submission_id
    where s.user_id = "4bd1135791ab4afe4d9f3215ea1705f8" AND r.compile_errors > '' """
    return query


def get_query_05():
    query = """ 
    SELECT  
    u.user_id, 
    category, 
    opl_ID, 
    SUM(nb_failed != 0) AS Failed_Submissions, 
    SUM(nb_failed = 0) AS Successfulll_Submissions, 
    SUM(r.style_result > '') AS amount_bad_style_submissions, 
    SUM(s.points_awarded) AS Points, 
    SUM(a.deadline * 10000 > s.timestamp) AS On_Time, 
    SUM(a.deadline * 10000 < s.timestamp) AS Too_Late, 
    language, 
    score_prolog, 
    score_haskell 
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
where timestamp < 202001310000 
GROUP BY u.user_id , category , language 
ORDER BY a.category ASC"""
    return query


def get_query_05_1617():
    query = """ 
   SELECT
    u.user_id,
    category,
    SUM(nb_failed != 0) AS Failed_Submissions,
    SUM(nb_failed = 0) AS Successfulll_Submissions,
    SUM(r.style_result > '') AS amount_bad_style_submissions,
    SUM(
        a.deadline * 10000 > s.timestamp
    ) AS On_Time,
    SUM(
        a.deadline * 10000 < s.timestamp
    ) AS Too_Late,
    a.language,
    g.score_prolog,
    g.score_haskell
FROM
    submissions AS s
INNER JOIN results AS r
ON
    r.submission_id = s.submission_id
INNER JOIN assignments AS a
ON
    a.assignment_id = s.assignment_id
INNER JOIN users AS u
ON
    u.user_id = s.user_id
INNER JOIN grades AS g
ON
    g.user_id = u.user_id

WHERE
    TIMESTAMP < 201701310000
GROUP BY
    u.user_id,
    category,
    LANGUAGE
ORDER BY
    a.category ASC"""
    return query

def get_query_05_1718():
    query = """ 
   SELECT
    u.user_id,
    category,
    SUM(nb_failed != 0) AS Failed_Submissions,
    SUM(nb_failed = 0) AS Successfulll_Submissions,
    SUM(r.style_result > '') AS amount_bad_style_submissions,
    SUM(
        a.deadline * 10000 > s.timestamp
    ) AS On_Time,
    SUM(
        a.deadline * 10000 < s.timestamp
    ) AS Too_Late,
    a.language,
    g.score_prolog,
    g.score_haskell
FROM
    submissions AS s
INNER JOIN results AS r
ON
    r.submission_id = s.submission_id
INNER JOIN assignments AS a
ON
    a.assignment_id = s.assignment_id
INNER JOIN users AS u
ON
    u.user_id = s.user_id
INNER JOIN grades AS g
ON
    g.user_id = u.user_id

WHERE
    TIMESTAMP < 201801310000
GROUP BY
    u.user_id,
    category,
    LANGUAGE
ORDER BY
    a.category ASC"""
    return query

def get_query_05_1819():
    query = """ 
   SELECT
    u.user_id,
    category,
    SUM(nb_failed != 0) AS Failed_Submissions,
    SUM(nb_failed = 0) AS Successfulll_Submissions,
    SUM(r.style_result > '') AS amount_bad_style_submissions,
    SUM(
        a.deadline * 10000 > s.timestamp
    ) AS On_Time,
    SUM(
        a.deadline * 10000 < s.timestamp
    ) AS Too_Late,
    a.language,
    g.score_prolog,
    g.score_haskell
FROM
    submissions AS s
INNER JOIN results AS r
ON
    r.submission_id = s.submission_id
INNER JOIN assignments AS a
ON
    a.assignment_id = s.assignment_id
INNER JOIN users AS u
ON
    u.user_id = s.user_id
INNER JOIN grades AS g
ON
    g.user_id = u.user_id

WHERE
    TIMESTAMP < 201901310000
GROUP BY
    u.user_id,
    category,
    LANGUAGE
ORDER BY
    a.category ASC"""
    return query

def get_query_06():
    query = """
SELECT
    r.compile_errors,r.nb_notimplemented,r.nb_failed,s.timestamp,a.category,a.assignment_id,a.language
FROM
    results AS r
INNER JOIN submissions AS s
ON
    r.submission_id = s.submission_id
INNER JOIN assignments AS a
ON
    a.assignment_id = s.assignment_id
WHERE
	s.user_id = "a706bb348b2a0c23e35ae11e4d68fc17" """
    return query

def get_query_06_2():
    query = """
SELECT
    r.compile_errors,a.category,a.assignment_id,a.language
FROM
    results AS r
INNER JOIN submissions AS s
ON
    r.submission_id = s.submission_id
INNER JOIN assignments AS a
ON
    a.assignment_id = s.assignment_id"""
    return query



def get_query_06_():
    query = """
SELECT
    s.user_id,r.compile_errors,a.category,a.assignment_id,a.language
FROM
    results AS r
INNER JOIN submissions AS s
ON
    r.submission_id = s.submission_id
INNER JOIN assignments AS a
ON
    a.assignment_id = s.assignment_id """
    return query


def get_query_07():
    msg = """
    SELECT r.compile_errors
    FROM results as r 
    INNER JOIN submissions as s on r.submission_id = s.submission_id 
    INNER JOIN assignments as a on a.assignment_id = s.assignment_id
    WHERE a.language = 2 AND s.user_id = "a706bb348b2a0c23e35ae11e4d68fc17" """
    return msg

def get_query_08_1920_all():
    query = """
SELECT
    s.user_id,r.compile_errors,a.category,a.assignment_id,a.language, nb_failed, style_result, s.points_awarded,
    s.timestamp, score_prolog, score_haskell,opl_ID, a.deadline , s.timestamp
FROM 
    esystant1920.submissions AS s 
        INNER JOIN 
    esystant1920.results AS r ON r.submission_id = s.submission_id 
        INNER JOIN 
    esystant1920.assignments AS a ON a.assignment_id = s.assignment_id 
        INNER JOIN 
    esystant1920.users AS u ON u.user_id = s.user_id 
        INNER JOIN 
    esystant1920.grades AS g ON g.user_id = u.user_id 
        INNER JOIN 
    esystant1920.education_type AS e ON e.KULopl = u.KULopl 
where timestamp < 202001310000 """
    return query

def get_query_08_1920_all_timestamp():
    query = """
SELECT
    s.user_id,r.compile_errors,a.category,a.assignment_id,a.language, nb_failed,nb_notimplemented, style_result, s.points_awarded,
    s.timestamp, score_prolog, score_haskell,opl_ID, a.deadline
FROM 
    esystant1920.submissions AS s 
        INNER JOIN 
    esystant1920.results AS r ON r.submission_id = s.submission_id 
        INNER JOIN 
    esystant1920.assignments AS a ON a.assignment_id = s.assignment_id 
        INNER JOIN 
    esystant1920.users AS u ON u.user_id = s.user_id 
        INNER JOIN 
    esystant1920.grades AS g ON g.user_id = u.user_id 
        INNER JOIN 
    esystant1920.education_type AS e ON e.KULopl = u.KULopl 
where timestamp < 202001310000 """
    return query

def get_query_08_1920_df(name_df):
    query = """
SELECT  
    user_id, 
    category, 
    opl_ID, 
    SUM(nb_failed != 0) AS Failed_Submissions, 
    SUM(nb_failed = 0) AS Successfulll_Submissions, 
    SUM(style_result > '') AS amount_bad_style_submissions, 
    SUM(points_awarded) AS Points, 
    SUM(deadline * 10000 > timestamp) AS On_Time, 
    SUM(deadline * 10000 < timestamp) AS Too_Late, 
    language, 
    score_prolog, 
    score_haskell 
FROM """ + name_df + """ 
GROUP BY user_id , category , language 
ORDER BY category ASC

    """
    return query