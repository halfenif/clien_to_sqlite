select seq, pubdate, regdate at time zone ('Asia/Seoul') from tb_article order by seq desc limit 1000;

select seq, title, pubdate, regdate AT TIME ZONE 'Asia/Seoul' from tb_article order by seq desc limit 100;
select regdate,
       regdate AT TIME ZONE 'Asia/Seoul',
       regdate AT TIME ZONE 'UTC',
       now(),
       now() AT TIME ZONE 'Asia/Seoul'
from tb_article where seq = 10794389 ;
--select regdate from tb_article order by seq desc limit 1000

select now() AT TIME ZONE 'Asia/Seoul';
select now();
-- '2017-06-12 09:56:48.715265+00'
-- '2017-06-12 10:52:20.058441+00'
-- '2017-06-12 10:51:49.230699'


select agentid, count(seq)
from   tb_article_index
where  1=1
--and    agentid >= 7001
--and    agentid <= 7100
and    workstate = 0
group by agentid
order by agentid
;

select   agentid
        ,lastseq
        ,(now() - lastupdate) updategap
        ,processid, subprocessid
from     tb_agent
where  agentid >= 7001
and    agentid <= 7100
order by agentid
;


select t.d, count(t.d) from (
select workstate || '-' || resultstate  as d
from   tb_article_index
) t
group by t.d
order by t.d
;

select * from tb_article_index
where  1=1
and    workstate = 0
and    resultstate = 400
--order by lastupdate desc
;
