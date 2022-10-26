import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

un = os.getenv('PYTHON_USERNAME')
pw = os.getenv('PYTHON_PASSWORD')
cs = os.getenv('PYTHON_CONNECTSTRING')
deveui='5CA05DEF6B070B04'

oracledb.init_oracle_client()

with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
    with connection.cursor() as cursor:
        req = '''
        BEGIN
        :result := tt.uni_bss.find_device_for_zabbix(p_deveui => '5CA05DEF6B070B04',
        p_tt_trouble => 'Проверка');
        commit;
        end;
        '''
        # sql = """select sysdate from dual"""
        for r in cursor.execute(req):
            print(r)
