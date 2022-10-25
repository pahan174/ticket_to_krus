import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

un = os.getenv('PYTHON_USERNAME')
pw = os.getenv('PYTHON_PASSWORD')
cs = os.getenv('PYTHON_CONNECTSTRING')

with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
    with connection.cursor() as cursor:
        sql = """select sysdate from dual"""
        for r in cursor.execute(sql):
            print(r)
