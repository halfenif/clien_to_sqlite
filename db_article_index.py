import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time

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
    print(maxseq)
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
    print(maxseq)
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
    cur.execute(query, params)
    conn.commit()
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
    cur.execute(query, params)
    conn.commit()
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
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
