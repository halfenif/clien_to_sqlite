import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam
import time
from itertools import count

import db_article_index


def get_target():
    set_target = set()

    conn = const_dbms.get_conn()
    cur = conn.cursor()
    query, params = utils.formatQuery(('SELECT seq FROM tb_article_index WHERE 1=',
                                        Param(1),
                                        'AND workstate = 0 ',
                                        'ORDER BY seq DESC'
                                        ),
                                       cur.paramstyle)
    cur.execute(query, params)

    for i, row in enumerate(cur.fetchall()):
        set_target.add(row['seq'])

        if (i % 1000) == 0:
            print('Target Make:', format(i,','))

    print('[ {} ][ Target Fetch End ][ {} ]'.format(time.strftime('%x %X', time.localtime()), format(len(set_target),',')))
    conn.close()
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

    for i, seq in enumerate(set_target):
        item['seq'] = seq
        item['bbsclass'] = const_config.get_bbs_class()
        item['agentid'] = const_config.get_start_port() + (i % const_config.get_agent_count())

        query, params = utils.formatQuery(('UPDATE tb_article_index SET ',
                                           'bbsclass=',  Param(item['bbsclass']),   ',',
                                           'agentid=',   Param(item['agentid']),
                                           'WHERE seq=', Param(item['seq'])
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
