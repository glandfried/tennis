select
m.match_id
,e.double
,m.round_number
,m.winner_player_1
,w1.player_name
,m.winner_player_2
,m.looser_player_1
,m.looser_player_2
,e.time_start
,e.time_end
,e.ground
,t.tour_id
,t.tour_name
from match m
inner join player w1
on m.winner_player_1 = w1.player_id
inner join player l1
on m.looser_player_1 = l1.player_id
left join player w2
on m.winner_player_2 = w2.player_id
left join player l2
on m.looser_player_2 = l2.player_id
inner join event e
on e.event_id = m.event_id
inner join tournament t
on e.tour_id = t.tour_id
order by e.time_start asc, m.round_number desc;


