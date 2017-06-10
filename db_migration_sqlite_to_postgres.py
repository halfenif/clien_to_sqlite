import dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time
import html

def get_conn_sqlite():
    return dbms.connect.sqlite('w:/data/sqlite/db_clien.db')

def get_conn_postgres():
    return dbms.connect.postgres('clien', 'clien', 'clien')

def delete_target():
    conn_postgres = get_conn_postgres()
    cur_postgres  = conn_postgres.cursor()
    query_postgres, params_postgres = utils.formatQuery(('DELETE FROM tb_article where 1=',Param(1)),cur_postgres.paramstyle)
    cur_postgres.execute(query_postgres, params_postgres)
    conn_postgres.commit()
    print('Target Deleted')
    return

def run_mig():
    conn_sqlit    = get_conn_sqlite()
    conn_postgres = get_conn_postgres()

    cur_sqlite    = conn_sqlit.cursor()
    cur_postgres  = conn_postgres.cursor()

    query_sqlite, params_sqlite = utils.formatQuery(('SELECT * FROM tb_article WHERE 1=', Param(1) ),
                                                    cur_sqlite.paramstyle)
    cur_sqlite.execute(query_sqlite, params_sqlite)


    cnt_total = 0
    cnt_not_commit = 0
    commit_level = 100000

    for row in cur_sqlite.fetchall():
        #print('row:', row)
        #print('1', row["title"])
        #print('2', row["title"].replace('\0',''))
        query_postgres, params_postgres = utils.formatQuery(('INSERT INTO tb_article (seq, title, body, pubdate, postuser, regdate) VALUES (',
                                            Param(row["seq"]),      ',',
                                            Param(html.unescape(row["title"].replace('\0','').strip())),    ',',
                                            Param(html.unescape(row["body"].replace('\0','').strip())),     ',',
                                            Param(row["pubdate"]),  ',',
                                            Param(row["postuser"]), ',',
                                            Param(row["regdate"]),  ')'
                                            ),
                                           cur_postgres.paramstyle)

        try:
            cur_postgres.execute(query_postgres, params_postgres)
        except Exception as e:
            print('Exception:', row)
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

        cnt_total += 1
        cnt_not_commit += 1

        if cnt_not_commit == commit_level:
            conn_postgres.commit()
            cnt_not_commit = 0
            print(time.strftime("%x %X"), format(cnt_total,','), 'Commited')

    #Last Commited
    conn_postgres.commit()
    print(time.strftime("%x %X"), format(cnt_total,','), 'Commited')
    return

#---------------------------------
# main Suit
if __name__ == "__main__":
    delete_target()
    run_mig()
