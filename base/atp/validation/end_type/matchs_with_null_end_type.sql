select t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1, end_type
from match m
inner join tournament t
on t.tournament_id = m.tournament_id
where m.end_type is null
;


