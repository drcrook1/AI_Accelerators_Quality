"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
import pyodbc
import os

def get_db_cxn() -> pyodbc.Connection:
    driver = os.environ["SQL_DRIVER"]
    server = os.environ["SQL_SERVER"]
    database = os.environ["SQL_DB"]
    username = os.environ["SQL_USER"]
    password = os.environ["SQL_PW"]
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn