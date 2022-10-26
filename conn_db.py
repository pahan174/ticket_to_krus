import os
import oracledb
from dotenv import load_dotenv
import sys
from pyzabbix import ZabbixAPI


load_dotenv()

un = os.getenv('PYTHON_USERNAME')
pw = os.getenv('PYTHON_PASSWORD')
cs = os.getenv('PYTHON_CONNECTSTRING')
URL_ZABBIX = os.getenv("URL_ZABBIX", default='127.0.0.1')
USER_ZABBIX = os.getenv("USER_ZABBIX", default='Admin')
USER_PASS = os.getenv("USER_PASS", default='Admin')

deveui = sys.argv[1]
text = sys.argv[2]
eventid = sys.argv[3]


def send_event_info(zapi, text, action) -> None:
    zapi.do_request('event.acknowledge',
                    {
                     'eventids': eventid,
                     'action': action,
                     'message': text
                     })


oracledb.init_oracle_client()
zapi = ZabbixAPI(url=URL_ZABBIX, user=USER_ZABBIX, password=USER_PASS)
try:
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            result = cursor.var(str)
            req = '''
            BEGIN
            :result := tt.uni_bss.find_device_for_zabbix(p_deveui => :p_deveui,
            p_tt_trouble => :p_tt_trouble);
            commit;
            end;
            '''

            cursor.execute(req, {
                    'p_deveui': deveui,
                    'p_tt_trouble': deveui + ' ' + text,
                    'result': result,
                })
except Exception as e:
    send_event_info(zapi, f'Нет связи с БД КРУС. Ошибка {e}', 4)
else:
    if 'no data found' in result.getvalue():
        send_event_info(zapi, 'Устройства нет в КРУС', 6)
    else:
        send_event_info(zapi, f'Номер тикета {result.getvalue()}', 6)
