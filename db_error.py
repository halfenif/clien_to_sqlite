import const_config
import dbms
import time

constDBMS = const_config.get_dbms()
constSQLInsert = 'INSERT INTO tb_error (seq) values (?)'
constSQLSelectForExistCheck = 'SELECT seq FROM tb_error WHERE seq = ?'

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
# SQL Eror Insert
def sqlInsert(result_index):

    conn = dbms.connect.sqlite(constDBMS)
    cur = conn.cursor()
    cur.execute(constSQLInsert, (result_index,))
    conn.commit()
    conn.close()
    return

#---------------------------------
# Error Logic - Insert or Skip
def insertItem(result_index):
    if sqlExistCheck(result_index):
        print('[Exist  Error] ' + str(result_index))
    else:
        sqlInsert(result_index)
        print('[Insert Error] ' + str(result_index))

    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    insertItem(const_config.testseqerror())
