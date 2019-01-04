#!/usr/bin/env python3
""" Code for getting the following details from News Database
  1. Top 3 Articles of All Time.
  2. Most Popular Article Authors of All Time.
  3. Days which had more than 1% Errors.
"""
import psycopg2

DBNAME = "news"


def get_queryResults(query):
    """Connect to news Database and return results of the provided query."""
    db = psycopg2.connect(database=DBNAME)
    dbcursor = db.cursor()
    dbcursor.execute(query)
    results = dbcursor.fetchall()
    db.close()
    return results


def get_top_Articles():
    """Return top 3 Articles from news Database."""
    print('<---Fetching Top 3 Popular Articles of All Time--->')
    query = "select title,count from Article_Views_Count limit 3"
    results = get_queryResults(query)
    for tup in results:
        print '{}-{} views'.format(*tup)
    print('\n')


def get_top_Authors():
    """Returns top Authors from news Database."""
    print('<---Fetching Popular Authors of All Time--->')
    query = '''select authors.name,AVC.views from authors,
               Author_Views_Count AVC
               where authors.id=AVC.author'''
    results = get_queryResults(query)
    for tup in results:
        print '{}-{} views'.format(*tup)
    print('\n')


def get_error_Prone_days():
    """Returns the days where news system received more than 1% Errors."""
    print('<---Fetching days which had more than 1 percent Errors--->')
    query = '''select to_char(day,'Mon DD,YYYY') as day,concat(percent,'%')
              as Error_Percent from (select * from Success_Error_Count) as qur
              where status not like '2%' and percent>1.000'''
    results = get_queryResults(query)
    for tup in results:
        print '{}-{}'.format(*tup)


if __name__ == '__main__':
    get_top_Articles()
    get_top_Authors()
    get_error_Prone_days()
