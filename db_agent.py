import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time

#---------------------------------
# SQL Exist Check
def sqlExistCheck(processid):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT processid FROM tb_agent WHERE processid = ',
                                       Param(processid)),
                                       cur.paramstyle)
    cur.execute(query, params)

    bExist = False
    if len(cur.fetchall())  > 0:
        bExist = True

    conn.close()
    return bExist


#---------------------------------
# SQL Article Index Insert
def sqlInsert(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_agent (processid) VALUES (',
                                        Param(item['processid']),  ')'
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)
    conn.commit()
    conn.close()
    return

#---------------------------------
# Agent update
def sqlUpdate(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('UPDATE tb_agent SET ',
                                       'lastseq=',           Param(item['seq']),         ',',
                                       'countok=',           Param(item['countok']),     ',',
                                       'countfail=',         Param(item['countfail']),   ',',
                                       'lastupdate= Now()',
                                       'WHERE processid=',   Param(item['processid'])
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)
    conn.commit()
    conn.close()
    return

#---------------------------------
# Agent Init
def sqlInitUpdate(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('UPDATE tb_agent SET ',
                                       'lastbbsclass=',      Param(const_config.get_bbs_class()), ',',
                                       'lastseq=',           Param(0),                            ',',
                                       'countok=',           Param(0),                            ',',
                                       'countfail=',         Param(0),                            ',',
                                       'begindate= Now()',                                        ',',
                                       'lastupdate= Now()',
                                       'WHERE processid=',   Param(item['processid'])
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)
    conn.commit()
    conn.close()
    return


#---------------------------------
# Agent Logic
def initAgent(item):
    if not sqlExistCheck(item['processid']):
        sqlInsert(item)
        print('[ {} ][ Insert Agent ][ {} ]'.format(time.strftime('%x %X', time.localtime()), item['processid']))

    sqlInitUpdate(item)

    return


#---------------------------------
# Agent Logic
def setAgent(item):
    if not sqlExistCheck(item['processid']):
        raise Exception('Init Agent First: ProcessId: {}'.format(item['processid']))

    sqlUpdate(item)

    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
