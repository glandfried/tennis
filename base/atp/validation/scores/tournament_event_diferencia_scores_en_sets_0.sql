select t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1
from sets s
inner join match m
on s.match_id = m.match_id
inner join tournament t
on t.tournament_id = m.tournament_id
where m.end_type = 'sets' and s.winner - s.looser = 0
group by  t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1;
