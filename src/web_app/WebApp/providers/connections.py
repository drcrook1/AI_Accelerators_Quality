"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
import pyodbc
import os
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

def get_db_cxn() -> pyodbc.Connection:
    driver = os.environ["SQL_DRIVER"]
    server = os.environ["SQL_SERVER"]
    database = os.environ["SQL_DB"]
    username = os.environ["SQL_USER"]
    password = os.environ["SQL_PW"]
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn

def get_tbl_cnxn():
    """
    gets an azure table storage connection
    """
    account_name = os.environ["STORAGE_ACCOUNT_NAME"]
    account_key = os.environ["STORAGE_ACCOUNT_KEY"]
    return TableService(account_name=account_name, account_key=account_key)
