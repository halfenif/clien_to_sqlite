import const_config
import const_dbms
import time


constSQLDeleteSummaryDay = 'DELETE FROM tb_summary_day'
tempSQL = []
tempSQL.append("INSERT INTO tb_summary_day (day, cnt) ")
tempSQL.append("SELECT day, count(day) cnt FROM ( ")
tempSQL.append("SELECT SUBSTR(pubdate, 1,10) day FROM tb_article ")
tempSQL.append(") ")
tempSQL.append("GROUP BY day ")
constSQLInsertSummaryDay = ''.join(tempSQL)

#---------------------------------
# SQL Summary Update
def sqlUpdateSummaryDay():
    conn = const_dbms.get_conn()
    cur = conn.cursor()
    cur.execute(constSQLDeleteSummaryDay)
    conn.commit()

    cur.execute(constSQLInsertSummaryDay)
    conn.commit()
    conn.close()
    return

#---------------------------------
# Test Suit
if __name__ == "__main__":
    sqlUpdateSummaryDay()
