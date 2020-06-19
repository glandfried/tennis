select m.end_type , count(*)
from match m
group by m.end_type;

/*

 end_type | count  
----------+--------
          |   1768
 sets     | 139554
 (RET)    |   2906
 (W/O)    |      3
 (ABD)    |     18
 (DEF)    |     26
 (UNP)    |      1
 (ABN)    |      2
 (NA)     |      2
 (WEA)    |      1
(10 rows)



select m.event_id, t.tournament_name, m.round_number, m.winner_player_1
from match m
inner join tournament t 
on t.tournament_id = m.tournament_id
where m.end_type is null;

*/
