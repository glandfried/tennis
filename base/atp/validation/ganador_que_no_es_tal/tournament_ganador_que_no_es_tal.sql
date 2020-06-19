with ganador_que_no_es_tal as (
	select t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1
	from sets s
	inner join match m
	on s.match_id = m.match_id
	inner join tournament t
	on t.tournament_id = m.tournament_id
	where m.end_type = 'sets'
	group by  t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1
	having sum(((s.winner - s.looser) > 0)::int) <= sum(((s.winner - s.looser) <= 0)::int)  
)

select tournament_name, tournament_id, year, double, count(*)
from ganador_que_no_es_tal g
group by tournament_name, tournament_id, year, double


