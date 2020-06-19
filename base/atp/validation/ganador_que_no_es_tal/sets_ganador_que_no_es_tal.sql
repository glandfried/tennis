with ganador_que_no_es_tal as (
	select t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1, m.match_id
	from sets s
	inner join match m
	on s.match_id = m.match_id
	inner join tournament t
	on t.tournament_id = m.tournament_id
	where m.end_type = 'sets'
	group by  t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1,  m.match_id
	having sum(((s.winner - s.looser) > 0)::int) <= sum(((s.winner - s.looser) <= 0)::int)  
) 

select g.*, s.set_number, s.winner, s.looser
from ganador_que_no_es_tal g
inner join sets s 
on s.match_id = g.match_id; 


