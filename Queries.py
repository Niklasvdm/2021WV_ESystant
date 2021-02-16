########################### PURPOSE OF FILE :
#
# Return a bunch of queries in stead of them being thrown randomly in files.
#
#



#
#
#
def getQuery01():
    query = """SELECT 
        u.user_id,
        category,
        SUM(nb_failed != 0) AS Failed_Submissions,
        SUM(nb_failed = 0) AS Successfulll_Submissions,
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


def getQuery02():
    query = """
    SELECT 
        u.user_id,
        category,
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
    GROUP BY user_id , category , language
    """
    return query

def getQuery03():
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
GROUP BY u.user_id , category, language
ORDER BY a.category ASC
    """
    return query

def getQuery04():
    query= """SELECT s.user_id,r.compile_errors
FROM results as r INNER JOIN submissions as s on s.submission_id = r.submission_id
where s.user_id = "4bd1135791ab4afe4d9f3215ea1705f8" """
    return query

def getQuery05():
    query= """
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

