import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time
from itertools import count

import db_article_index

def get_all():
    set_all = set()
    for i in range(db_article_index.sqlGetMaxSeq()):
        set_all.add(i)

    return set_all

def get_source():
    set_source = set()

    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT seq FROM tb_article_index WHERE 1=',
                                        Param(1)
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)

    for row in cur.fetchall():
        set_source.add(row['seq'])

    print('[ {} ][ Source Fetch End ][ {} ]'.format(time.strftime('%x %X', time.localtime()), format(len(set_source),',')))
    return set_source

def get_target():
    set_all = get_all()
    set_source = get_source()
    set_target = set_all.difference(set_source)

    print('[ {} ][ Target Build End ][ {} ]'.format(time.strftime('%x %X', time.localtime()), format(len(set_target),',')))
    return set_target

def main():
    print('[ {} ][ Begin ]'.format(time.strftime('%x %X', time.localtime())))

    #Make Target
    set_target = get_target()

    #Loop Connection
    conn = const_dbms.get_conn()
    cur = conn.cursor()

    #init Value
    cnt_total = 0
    cnt_not_commit = 0
    commit_level = 100000
    item = {}

    for seq in set_target:
        item['seq'] = seq
        item['bbsclass'] = const_config.get_bbs_class()
        item['processid'] = const_config.get_start_port()

        query, params = utils.formatQuery(('INSERT INTO tb_article_index (seq, bbsclass, processid) VALUES (',
                                            Param(item['seq']),        ',',
                                            Param(item['bbsclass']),   ',',
                                            Param(item['processid']),  ')'
                                            ),
                                           cur.paramstyle)
        cur.execute(query, params)

        cnt_total += 1
        cnt_not_commit += 1

        if cnt_not_commit == commit_level:
            conn.commit()
            cnt_not_commit = 0
            print('[ {} ][ Processing Commited ][ {} ][ {}% ]'.format(time.strftime('%x %X', time.localtime()), format(cnt_total,','), round((cnt_total/len(set_target)*100),2)))

    #Last Commited
    conn.commit()
    print('[ {} ][ End Commited ][ {} ][ {}% ]'.format(time.strftime('%x %X', time.localtime()), format(cnt_total,','), round((cnt_total/len(set_target)*100),2)))

if __name__ == '__main__':
    main()
