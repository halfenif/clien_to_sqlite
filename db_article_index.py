import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time
import psycopg2

#---------------------------------
# SQL Exist Check
def sqlExistCheck(seq):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT seq FROM tb_article_index WHERE seq = ',
                                       Param(seq)),
                                       cur.paramstyle)
    cur.execute(query, params)

    bExist = False
    if len(cur.fetchall())  > 0:
        bExist = True

    conn.close()
    return bExist

#---------------------------------
# SQL Max Seq
def sqlGetMaxSeq():
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT MAX(seq) seq FROM tb_article_index WHERE 1=', Param(1) ),
                                       cur.paramstyle)
    cur.execute(query, params)
    maxseq = cur.fetchone()
    conn.close()

    if maxseq['seq'] == None:
        return 0
    return maxseq['seq']

#---------------------------------
# SQL Min Seq
def sqlGetMinSeq():
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT MIN(seq) seq FROM tb_article_index WHERE 1=', Param(1) ),
                                       cur.paramstyle)
    cur.execute(query, params)
    maxseq = cur.fetchone()
    conn.close()

    if maxseq['seq'] == None:
        return 0
    return maxseq['seq']

#---------------------------------
# SQL Article Index Insert
def sqlInsert(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_article_index (seq, bbsclass, agentid) VALUES (',
                                        Param(item['seq']),        ',',
                                        Param(item['bbsclass']),   ',',
                                        Param(item['agentid']),    ')'
                                        ),
                                       cur.paramstyle)

    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        print("db_article_index.sqlInsert.psycopg2.IntegrityError:{}".format(err.pgcode))
    except Exception as err:
        print("db_article_index.sqlInsert.Other Exception:{}".format(err))
    else:
        conn.commit()
    finally:
        conn.close()

    return

#---------------------------------
# SQL Article Index update
def sqlUpdate(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('UPDATE tb_article_index SET ',
                                       'bbsclass=',    Param(item['bbsclass']),    ',',
                                       'agentid=',     Param(item['agentid']),     ',',
                                       'workstate=',   Param(item['workstate']),   ',',
                                       'resultstate=', Param(item['resultstate']), ',',
                                       'lastupdate= Now() '
                                       'WHERE seq=',   Param(item['seq'])
                                        ),
                                       cur.paramstyle)
    try:
        cur.execute(query, params)
    except psycopg2.IntegrityError as err:
        print("db_article_index.sqlUpdate.psycopg2.IntegrityError:{}".format(err.pgcode))
    except Exception as err:
        print("db_article_index.sqlUpdate.Other Exception:{}".format(err))
    else:
        conn.commit()
    finally:
        conn.close()
    return

#---------------------------------
# Article Logic - Insert or Skip
def insertItem(item):
    if sqlExistCheck(item['seq']):
        print('[ {} ][ Exist  Article Index ][ {} ]'.format(time.strftime('%x %X', time.localtime()), item['seq']))
    else:
        sqlInsert(item)
        print('[ {} ][ Insert Article Index ][ {} ]'.format(time.strftime('%x %X', time.localtime()), item['seq']))
    return


#---------------------------------
# Make Target
def getTarget(item):
    target = []

    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT seq, bbsclass FROM tb_article_index WHERE workstate = 0 AND agentid = ',
                                       Param(item['agentid']),
                                       ' ORDER BY seq DESC LIMIT ' + str(const_config.get_target_make_count())
                                       ),
                                       cur.paramstyle)
    cur.execute(query, params)

    for result in cur.fetchall():
        target.append(result)

    print('[ {} ][ Make Target Result ][ {} ]'.format(time.strftime('%x %X', time.localtime()), format(len(target),',')))
    conn.close()

    return target

#---------------------------------
# SQL Exist Check for Update
def sqlExistCheckForStatusUpdate(bbsclass, seq):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT bbsclass, workstate, resultstate, agentid FROM tb_article_index WHERE seq = ',
                                       Param(seq)),
                                       cur.paramstyle)
    cur.execute(query, params)
    search_item = cur.fetchone()
    conn.close()

    db_result = 1 # Success
    #DB for Insert or Update
    item = {}
    item['seq'] = seq
    item['bbsclass'] = bbsclass
    item['agentid'] = const_config.get_start_port() + (seq % const_config.get_agent_count()) #For new item
    item['workstate'] = 0
    item['resultstate'] = 0

    if search_item == None:
        sqlInsert(item)
        print("[ {} ][ {} ][ {} ][ {} ][ {} ]".format(time.strftime('%x %X', time.localtime()),
                                               'Insert New'.ljust(19),
                                               item['agentid'],
                                               format(item['seq'],","),
                                               bbsclass
                                               ))
    elif search_item['workstate'] == 1 and search_item['resultstate'] != 200:
        item['agentid'] = search_item['agentid']
        sqlUpdate(item)
        print("[ {} ][ {} ][ {} ][ {} ][ {} ]".format(time.strftime('%x %X', time.localtime()),
                                               'Update Not 200'.ljust(19),
                                               item['agentid'],
                                               format(item['seq'],","),
                                               bbsclass
                                               ))
    elif search_item['workstate'] == 9:
        item['agentid'] = search_item['agentid']
        sqlUpdate(item)
        print("[ {} ][ {} ][ {} ][ {} ][ {} ]".format(time.strftime('%x %X', time.localtime()),
                                               'Update for 9'.ljust(19),
                                               item['agentid'],
                                               format(item['seq'],","),
                                               bbsclass
                                               ))
    else :
        msg = 'Skip:' + str(search_item['workstate']) + '/' + str(search_item['resultstate'])
        print("[ {} ][ {} ][ {} ][ {} ][ {} ]".format(time.strftime('%x %X', time.localtime()),
                                               msg.ljust(19),
                                               item['agentid'],
                                               format(item['seq'],","),
                                               bbsclass
                                               ))
        db_result = 0 # Skip

    return db_result


#---------------------------------
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
