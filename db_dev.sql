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
