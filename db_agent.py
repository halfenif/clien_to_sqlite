import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time
import psycopg2

#---------------------------------
# SQL Exist Check
def sqlExistCheck(agentid):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT agentid FROM tb_agent WHERE agentid = ',
                                       Param(agentid)),
                                       cur.paramstyle)
    cur.execute(query, params)

    bExist = False
    if len(cur.fetchall())  > 0:
        bExist = True

    conn.close()
    return bExist


#---------------------------------
# SQL Agent Insert
def sqlInsert(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_agent (agentid) VALUES (',
                                        Param(item['agentid']),  ')'
                                        ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        print("db_agent.sqlInsert.psycopg2.IntegrityError:{}".format(err.pgcode))
    except Exception as err:
        print("db_agent.sqlInsert.Other Exception:{}".format(err))
    else:
        conn.commit()
    finally:
        conn.close()
    return

#---------------------------------
# SQL Agent History
def sqlInsertHist(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_agent_hist',
                                       "SELECT nextval('seq_agent_hist'), agentid, processid, lastseq, lastbbsclass, countok, countfail, begindate, lastupdate FROM tb_agent WHERE agentid=",
                                        Param(item['agentid'])
                                        ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        print("db_agent.sqlInsertHist.psycopg2.IntegrityError:{}".format(err.pgcode))
    except Exception as err:
        print("db_agent.sqlInsertHist.Other Exception:{}".format(err))
    else:
        conn.commit()
    finally:
        conn.close()
    return

#---------------------------------
# Agent update
def sqlUpdate(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('UPDATE tb_agent SET ',
                                       'processid=',         Param(item['processid']),   ',',
                                       'lastseq=',           Param(item['seq']),         ',',
                                       'countok=',           Param(item['countok']),     ',',
                                       'countfail=',         Param(item['countfail']),   ',',
                                       'lastupdate= Now()',
                                       'WHERE agentid=',   Param(item['agentid'])
                                        ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        print("db_agent.sqlUpdate.psycopg2.IntegrityError:{}".format(err.pgcode))
    except Exception as err:
        print("db_agent.sqlUpdate.Other Exception:{}".format(err))
    else:
        conn.commit()
    finally:
        conn.close()
    return

#---------------------------------
# Agent Init
def sqlInitUpdate(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('UPDATE tb_agent SET ',
                                       'processid=',         Param(0),                            ',',
                                       'lastbbsclass=',      Param(const_config.get_bbs_class()), ',',
                                       'lastseq=',           Param(0),                            ',',
                                       'countok=',           Param(0),                            ',',
                                       'countfail=',         Param(0),                            ',',
                                       'begindate= Now()',                                        ',',
                                       'lastupdate= Now()',
                                       'WHERE agentid=',   Param(item['agentid'])
                                        ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        print("db_agent.sqlInitUpdate.psycopg2.IntegrityError:{}".format(err.pgcode))
    except Exception as err:
        print("db_agent.sqlInitUpdate.Other Exception:{}".format(err))
    else:
        conn.commit()
    finally:
        conn.close()
    return


#---------------------------------
# Agent Logic
def initAgent(item):
    if not sqlExistCheck(item['agentid']):
        sqlInsert(item)
        print('[ {} ][ Insert Agent ][ {} ]'.format(time.strftime('%x %X', time.localtime()), item['agentid']))

    sqlInitUpdate(item)
    return

def logAgent(item):
    sqlInsertHist(item)
    return

#---------------------------------
# Agent Logic
def setAgent(item):
    if not sqlExistCheck(item['agentid']):
        raise Exception('Init Agent First: AgentId: {}'.format(item['agentid']))

    sqlUpdate(item)

    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
