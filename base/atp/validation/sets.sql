with max_set as (
 select max(s.set_number) as zero, s.match_id
 from sets s
 inner join match m
 on s.match_id = m.match_id
 where m.end_type = 'sets'
 group by s.match_id 
)

select distinct m.match_id
from match m
inner join max_set ms
on m.match_id = ms.match_id
where ms.zero = 0
