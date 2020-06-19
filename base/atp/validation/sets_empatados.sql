select t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1
from sets s
inner join match m
on s.match_id = m.match_id
inner join tournament t
on t.tournament_id = m.tournament_id
where m.end_type = 'sets' and s.winner - s.looser = 0
group by  t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1;


/*
 moscow,438,2008,f,7,kb54
 wimbledon,540,1965,f,6,r055
 washington,418,2007,f,5,h442
 umag,439,1993,f,3,m412
*/
