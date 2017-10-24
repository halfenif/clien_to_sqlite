select '7000', count(seq) from tb_article_index where agentid = 7000 and workstate = 0 union all
select '7996', count(seq) from tb_article_index where agentid = 7996 and workstate = 0 union all
select '7997', count(seq) from tb_article_index where agentid = 7997 and workstate = 0
;

select max(tt.seq) from (
select t.seq from (
select seq from tb_article_index
where 1=1
and   agentid = 7000
and   workstate = 0
order by seq asc
) t
limit 10000
) tt
;

--11124017
--11134966

--select count(seq) from tb_article_index
update tb_article_index
set agentid = 7996
where 1=1
and   seq <= 11134966
and   workstate = 0
and   agentid = 7000
;

commit;
