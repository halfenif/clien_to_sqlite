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
# SQL Article Insert
def sqlInsert(result_index, result_bbsclass, collectpage, processid):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_article_index (seq, bbsclass, collectpage, processid) VALUES (',
                                        Param(result_index),     ',',
                                        Param(result_bbsclass),  ',',
                                        Param(collectpage),      ',',
                                        Param(processid),        ')'
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)

    #cur.execute(constSQLInsert, (result_index, result_title, result_body, result_date_for_key, result_user,))
    conn.commit()
    conn.close()
    return

#---------------------------------
# Article Logic - Insert or Skip
def insertItem(result_index, result_bbsclass, collectpage, processid):
    if sqlExistCheck(result_index):
        print('[Exist  Article Index] ', result_index, result_bbsclass)
    else:
        sqlInsert(result_index, result_bbsclass, collectpage, processid)
        #print('[Insert Article] ' + result_date_for_key + ':' + result_title)
        print('[', time.strftime('%x %X', time.localtime()),']', 'Insert Article Index', result_bbsclass, result_index)
    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
