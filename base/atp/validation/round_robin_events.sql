select distinct m.event_id, tournament_name
from match m 
inner join tournament t
on m.tournament_id = t.tournament_id
where m.round_name like 'Round Robin';
/*
 event_id | tournament_name  
----------+------------------
 60519710 | nitto-atp-finals
 60519700 | nitto-atp-finals
*/

