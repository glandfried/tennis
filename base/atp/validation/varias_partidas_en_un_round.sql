select event_id, round_name, player_id, count(*)
from (
	select winner_player_1 as player_id, looser_player_1 as oponent, event_id, round_name
	from match
	union
	select looser_player_1 as player_id, winner_player_1 as oponent, event_id, round_name
	from match
	union
	select winner_player_2 as player_id, looser_player_1 as oponent, event_id, round_name
	from match
	union
	select looser_player_2 as player_id, winner_player_1 as oponent, event_id, round_name
	from match
) q
where q.player_id is not null
group by event_id, round_name, player_id
having count(*)>1;

/*
 event_id |  round_name  | player_id | count 
----------+--------------+-----------+-------
 35220010 | Round of 64  | 0         |     2
 42219690 | Round of 128 | d246      |     2   (Player Unknown)
 60519700 | Round Robin  | a063      |     5
 60519700 | Round Robin  | f074      |     5
 60519700 | Round Robin  | k049      |     5
 60519700 | Round Robin  | l058      |     4
 60519700 | Round Robin  | r075      |     5
 60519700 | Round Robin  | s060      |     4
 60519710 | Round Robin  | b122      |     6
 60519710 | Round Robin  | f074      |     6
 60519710 | Round Robin  | g079      |     6
 60519710 | Round Robin  | k049      |     6
 60519710 | Round Robin  | n008      |     5
 60519710 | Round Robin  | r071      |     6
 60519710 | Round Robin  | s060      |     5
*/



