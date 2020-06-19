select tournament_id, year, double
from sets s
inner join match m
on s.match_id = m.match_id
where s.winner - s.looser = 0
group by tournament_id, year, double;
