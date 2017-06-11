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


#Postgres Table
# DROP TABLE public.tb_article;
#
# CREATE TABLE public.tb_article
# (
#     seq integer NOT NULL,
#     title text COLLATE pg_catalog."default",
#     body text COLLATE pg_catalog."default",
#     pubdate text COLLATE pg_catalog."default",
#     postuser text COLLATE pg_catalog."default",
#     regdate timestamp without time zone DEFAULT timestamp 'now()' NOT NULL,
#     CONSTRAINT tb_article_pkey PRIMARY KEY (seq)
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE clien;
#
# ALTER TABLE public.tb_article
#     OWNER to clien;


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
