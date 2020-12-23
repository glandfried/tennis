select m.match_id, s.set_number
,e.double
,m.round_number
,m.winner_player_1
,m.winner_player_2
,s.winner > s.looser as res
,m.looser_player_1
,m.looser_player_2
,e.time_start
,e.time_end
from match m 
inner join event e
on e.event_id = m.event_id
inner join sets s
on m.match_id = s.match_id
where (s.winner > 3 or s.looser > 3)
  and s.winner <> s.looser
