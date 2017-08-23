import dbms
import os

#Postgres Table
DROP TABLE public.tb_article;

CREATE TABLE public.tb_article
(
    seq integer NOT NULL,
    bbsclass text COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default",
    body text COLLATE pg_catalog."default",
    pubdate text COLLATE pg_catalog."default",
    postuser text COLLATE pg_catalog."default",
    ip text COLLATE pg_catalog."default",
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

INSERT INTO tb_article
SELECT seq, 'park', title, body, pubdate, postuser, regdate FROM tb_article_backup;

commit;

#----------------------------------

DROP TABLE public.tb_article_index;

CREATE TABLE public.tb_article_index
(
    seq integer NOT NULL,
    bbsclass text COLLATE pg_catalog."default" NOT NULL,
    agentid integer NOT NULL,
    workstate integer NOT NULL,
    resultstate integer NOT NULL,
    regdate timestamp with time zone NOT NULL,
    lastupdate timestamp with time zone NOT NULL,
    CONSTRAINT tb_article_index_pkey PRIMARY KEY (seq)
)
WITH (
    OIDS = FALSE
)
TABLESPACE clien;
-- Work State
-- 0 Target
-- 1 Complete
-- Result State = Request Result
ALTER TABLE public.tb_article_index
    OWNER to clien;


ALTER TABLE public.tb_article_index
    ALTER COLUMN regdate SET DEFAULT now();

ALTER TABLE public.tb_article_index
    ALTER COLUMN lastupdate SET DEFAULT now();

ALTER TABLE public.tb_article_index
    ALTER COLUMN workstate SET DEFAULT 0;

ALTER TABLE public.tb_article_index
    ALTER COLUMN resultstate SET DEFAULT 0;

CREATE INDEX CONCURRENTLY tb_article_index_processid
    ON public.tb_article_index(agentid, workstate, seq);

CREATE INDEX CONCURRENTLY tb_article_index_workstate
    ON public.tb_article_index(workstate, seq);

INSERT INTO tb_article_index
SELECT seq, bbsclass, 7000, 1, 200, regdate, regdate from tb_article;

update tb_article_index set workstate = 9 where workstate = 0 and seq > 6000000; --2,589,799

commit;

#----------------------------------
DROP TABLE public.tb_agent;

CREATE TABLE public.tb_agent
(
    agentid integer NOT NULL,
    processid integer NOT NULL,
    subprocessid integer NOT NULL,
    lastseq integer NOT NULL,
    countloop integer NOT NULL,
    countok integer NOT NULL,
    countfail integer NOT NULL,
    begindate timestamp with time zone NOT NULL,
    lastupdate timestamp with time zone NOT NULL,
    CONSTRAINT tb_agent_pkey PRIMARY KEY (agentid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE clien;

ALTER TABLE public.tb_agent
    OWNER to clien;

ALTER TABLE public.tb_agent
    ALTER COLUMN processid SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN subprocessid SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN lastseq SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN lastseq SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN countloop SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN countok SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN countfail SET DEFAULT 0;

ALTER TABLE public.tb_agent
    ALTER COLUMN begindate SET DEFAULT now();

ALTER TABLE public.tb_agent
    ALTER COLUMN lastupdate SET DEFAULT now();

#----------------------------------
DROP TABLE public.tb_agent_hist;

CREATE TABLE public.tb_agent_hist
(
    seq integer NOT NULL,
    agentid integer NOT NULL,
    processid integer NOT NULL,
    subprocessid integer NOT NULL,
    lastseq integer NOT NULL,
    countloop integer NOT NULL,
    countok integer NOT NULL,
    countfail integer NOT NULL,
    begindate timestamp with time zone NOT NULL,
    lastupdate timestamp with time zone NOT NULL,
    CONSTRAINT tb_agent_hist_pkey PRIMARY KEY (seq)
)
WITH (
    OIDS = FALSE
)
TABLESPACE clien;

ALTER TABLE public.tb_agent_hist
    OWNER to clien;

#----------------------------------
DROP SEQUENCE public.seq_agent_hist CASCADE;

CREATE SEQUENCE public.seq_agent_hist;

ALTER SEQUENCE seq_agent_hist RESTART WITH 16891; #select max(seq) from tb_agent_hist;

# ALTER TABLE public.tb_agent_hist
#     ALTER COLUMN seq SET DEFAULT nextval('seq_agent_hist');
#
# ALTER SEQUENCE seq_agent_hist OWNED BY public.tb_agent_hist.seq;









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
