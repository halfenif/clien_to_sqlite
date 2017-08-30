import datetime
import codecs
import os
import const_config
import const_dbms
from dbms import utils
from dbms.utils import Param, NamedParam, cursorToCSV, cursorToJSON
import time
from itertools import count

query = """
select  a.seq
       ,a.postuser
       ,a.ip
       ,a.pubdate
from    tb_article        a
       ,tb_article_index  b
where   a.seq = b.seq
and     b.workstate = 0
and     b.resultstate = 400
"""

def get_filename(ext):
    constDateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    constCharSet = 'UTF-8'
    constOutputFolder = './output_response/'

    # Folder Safe
    try:
        os.stat(constOutputFolder)
    except:
        os.makedirs(constOutputFolder)

    write_date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_full_path = constOutputFolder + 'export' + '.' + write_date_time + '.' + ext
    return file_full_path

def main():
    print(query)
    print('-------------------------------------------------------------------')
    print('Begin')

    #Loop Connection
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    cur.execute(query)
    #cursorToCSV(cur, get_filename('csv'))
    cursorToJSON(cur, get_filename('json'))

    print('End')
    print('-------------------------------------------------------------------')



if __name__ == '__main__':
    main()
