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

constDBSummaryDay = (
    "CREATE TABLE `tb_summary_day` (                        "
    "	`day`	TEXT PRIMARY KEY,                           "
    "	`cnt`	INTEGER,                                    "
    "	`regdate`	datetime DEFAULT CURRENT_TIMESTAMP      "
    ")                                                      "
)

constDBError = (
    "CREATE TABLE `tb_error` (                              "
    "	`seq`	INTEGER PRIMARY KEY,                        "
    "	`status` TEXT,                                      "
    "	`regdate`	datetime DEFAULT CURRENT_TIMESTAMP,     "
    "	`checkdate`	datetime                                "
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
cur.execute(constDBError)

conn.commit()
conn.close()
