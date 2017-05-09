import dbms
import os
constOutputFolder = './output_dbms'
constDBMS = './output_dbms/db_clien.db'

constDBArticle = (
    "CREATE TABLE `tb_article` (                            "
    "	`seq`	INTEGER PRIMARY KEY,                        "
    "	`title`	TEXT,                                       "
    "	`body`	TEXT,                                       "
    "	`pubdate`	TEXT,                                   "
    "	`postuser`	TEXT,                                   "
    "	`regdate`	datetime DEFAULT CURRENT_TIMESTAMP      "
    ")                                                      "
)


#---------------------------------
# Folder Safe
try:
    os.stat(constOutputFolder)
except:
    os.makedirs(constOutputFolder)

#---------------------------------
# Create Table
conn = dbms.connect.sqlite(constDBMS)
cur = conn.cursor()

cur.execute(constDBArticle)

conn.commit()
conn.close()
