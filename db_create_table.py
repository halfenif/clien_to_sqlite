import dbms
import os

#Postgres Table
DROP TABLE public.tb_article;

CREATE TABLE public.tb_article
(
    seq integer NOT NULL,
    title text COLLATE pg_catalog."default",
    body text COLLATE pg_catalog."default",
    pubdate text COLLATE pg_catalog."default",
    postuser text COLLATE pg_catalog."default",
    stat integer NOT NULL,
    processid integer NOT NULL,
    regdate timestamp with time zone NOT NULL,
    CONSTRAINT tb_article_pkey PRIMARY KEY (seq)
)
WITH (
    OIDS = FALSE
)
TABLESPACE clien;

ALTER TABLE public.tb_article
    OWNER to clien;

ALTER TABLE public.tb_article
    ALTER COLUMN regdate SET DEFAULT now();

ALTER TABLE public.tb_article
    ALTER COLUMN stat SET DEFAULT 1;

CREATE INDEX CONCURRENTLY idx_processid
    ON public.tb_article(processid, seq);

# DROP TABLE public.tb_article_index;
#
# CREATE TABLE public.tb_article_index
# (
#     seq integer NOT NULL,
#     bbsclass text COLLATE pg_catalog."default",
#     stat integer NOT NULL,
#     collectpage integer NOT NULL,
#     processid integer NOT NULL,
#     regdate timestamp with time zone NOT NULL,
#     CONSTRAINT tb_article_index_pkey PRIMARY KEY (seq)
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE clien;
#
# ALTER TABLE public.tb_article_index
#     OWNER to clien;
#
#
# ALTER TABLE public.tb_article_index
#     ALTER COLUMN regdate SET DEFAULT now();
#
# ALTER TABLE public.tb_article_index
#     ALTER COLUMN stat SET DEFAULT 1;



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
