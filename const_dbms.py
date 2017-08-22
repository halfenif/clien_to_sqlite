import const_config
import dbms

def get_conn():
    return dbms.connect.postgres('clien', 'clien', 'clien', host="192.168.0.104")
    #return dbms.connect.postgres('clien', 'clien', 'clien')
