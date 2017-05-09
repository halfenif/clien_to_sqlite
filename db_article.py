import const_config
import dbms
import time

constDBMS = const_config.get_dbms()
constSQLInsert = 'INSERT INTO tb_article (seq, title, body, pubdate, postuser) values (?, ?, ?, ?, ?)'
constSQLSelectForExistCheck = 'SELECT seq FROM tb_article WHERE seq = ?'
constSQLSelectForMaxSeq = 'SELECT IFNULL(MAX(seq),0) maxseq FROM tb_article'
constSQLSelectForMinSeq = 'SELECT IFNULL(MIN(seq),0) minseq FROM tb_article'

#---------------------------------
# SQL Exist Check
def sqlExistCheck(seq):
    #print('sqlExistCheck')
    conn = dbms.connect.sqlite(constDBMS)
    cur = conn.cursor()
    cur.execute(constSQLSelectForExistCheck, (seq,))

    bExist = False

    if len(cur.fetchall())  > 0:
        bExist = True

    conn.close()
    return bExist


#---------------------------------
# SQL Max Seq
def sqlGetMaxSeq():
    conn = dbms.connect.sqlite(constDBMS)
    cur = conn.cursor()
    cur.execute(constSQLSelectForMaxSeq)
    maxseq = cur.fetchone()
    conn.close()

    return maxseq['maxseq']

#---------------------------------
# SQL Min Seq
def sqlGetMinSeq():
    conn = dbms.connect.sqlite(constDBMS)
    cur = conn.cursor()
    cur.execute(constSQLSelectForMinSeq)
    maxseq = cur.fetchone()
    conn.close()

    return maxseq['minseq']

#---------------------------------
# SQL Article Insert
def sqlInsert(result_index, result_title, result_body, result_date_for_key, result_user):

    conn = dbms.connect.sqlite(constDBMS)
    cur = conn.cursor()
    cur.execute(constSQLInsert, (result_index, result_title, result_body, result_date_for_key, result_user,))
    conn.commit()
    conn.close()
    return

#---------------------------------
# Article Logic - Insert or Skip
def insertItem(result_index, result_title, result_body, result_date_for_key, result_user):
    if sqlExistCheck(result_index):
        print('[Exist  Article] ' + result_title)
    else:
        sqlInsert(result_index, result_title, result_body, result_date_for_key, result_user)
        print('[Insert Article] ' + result_date_for_key + ':' + result_title)

    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    if sqlExistCheck(const_config.testseq()):
        print('Exist Data!')
    else:
        print('New Data')
