select t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1
from sets s
inner join match m
on s.match_id = m.match_id
inner join tournament t
on t.tournament_id = m.tournament_id
where m.end_type = 'sets'
group by  t.tournament_name, m.tournament_id, year, double, round_number, winner_player_1
having sum(((s.winner - s.looser) > 0)::int) <= sum(((s.winner - s.looser) <= 0)::int)  
;

/*
tournament_name,tournament_id,year,double,round_number,winner_player_1
acapulco,807,2007,f,3,m605
australian-open,580,1975,f,5,t096
australian-open,580,1995,f,5,r237
australian-open,580,1997,f,5,m475
australian-open,580,2007,f,9,p624
bastad,316,1994,f,4,j098
gstaad,314,2006,f,3,k435
hamburg,414,1969,f,1,o032
london,311,2002,t,1,b471
moscow,438,2008,f,7,kb54
new-york,424,2002,t,3,g352
rome,416,1986,f,5,p021
stockholm,429,2000,f,2,g379
umag,439,1993,f,3,m412
us-open,560,1971,f,4,a014
us-open,560,1981,f,3,k024
us-open,560,1990,f,6,h251
us-open,560,2001,f,6,c433
us-open,560,2001,f,6,g354
us-open,560,2002,f,6,s572
washington,418,1990,f,5,o098
washington,418,2000,t,4,b484
washington,418,2007,f,5,h442
wimbledon,540,1925,f,3,bo24
wimbledon,540,1965,f,6,r055
wimbledon,540,1973,f,5,h066
wimbledon,540,1992,f,6,k156
*/
