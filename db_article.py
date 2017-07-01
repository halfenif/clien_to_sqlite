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
    query, params = utils.formatQuery(('SELECT seq FROM tb_article WHERE seq = ',
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
    query, params = utils.formatQuery(('SELECT MAX(seq) seq FROM tb_article WHERE 1=', Param(1) ),
                                       cur.paramstyle)
    cur.execute(query, params)
    returnseq = cur.fetchone()
    conn.close()

    if returnseq['seq'] == None:
        return 0
    return returnseq['seq']

#---------------------------------
# SQL Min Seq
def sqlGetMinSeq(processid=0):
    if processid == 0:
        processid = const_config.get_start_port()

    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT MIN(seq) seq FROM tb_article WHERE processid=', Param(processid) ),
                                       cur.paramstyle)
    cur.execute(query, params)
    returnseq = cur.fetchone()
    conn.close()

    if returnseq['seq'] == None:
        return 0

    return returnseq['seq']

#---------------------------------
# SQL Article Insert
def sqlInsert(item):
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('INSERT INTO tb_article (seq, bbsclass, title, body, pubdate, postuser ) VALUES (',
                                        Param(item['seq']),       ',',
                                        Param(item['bbsclass']),  ',',
                                        Param(item['title']),     ',',
                                        Param(item['body']),      ',',
                                        Param(item['pubdate']),   ',',
                                        Param(item['postuser']),  ')'
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)
    conn.commit()
    conn.close()
    return

#---------------------------------
# Article Logic - Insert or Skip
def insertItem(item):
    #
    if sqlExistCheck(item['seq']):
        print('[Exist  Article] ' + item['title'])
    else:
        sqlInsert(item)
        print("[ {} ][ {} ][ {} ][ {} ] {}".format(time.strftime('%x %X', time.localtime()), item['pubdate'], item['agentid'], item['seq'], item['title']))
    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
