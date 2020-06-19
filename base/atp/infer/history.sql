select m.match_id
,e.double
,m.round_number
,m.winner_player_1
,m.winner_player_2
,m.looser_player_1
,m.looser_player_2
,e.time_start
,e.time_end
from match m 
inner join event e
on e.event_id = m.event_id

