select t.tournament_name, m.tournament_id,year, double, round_number, winner_player_1,  match_id
from match m
inner join tournament t
on t.tournament_id = m.tournament_id
where m.looser_player_1 ='0';

/*
shenzhen,6967,2015,f,6,bd82,124605
paris,352,2001,f,5,k293,119357
paris,352,2001,f,5,r485,119358
australian-open,580,1923,f,3,o591,106473
australian-open,580,1915,f,3,hf22,137888
australian-open,580,1922,f,4,bq82,139075
australian-open,580,1922,f,5,bq82,139088
london,311,1969,f,6,b224,42505
atlanta,6116,2015,f,7,cg49,28969
*/

select t.tournament_name, m.tournament_id,year, double, round_number, winner_player_1,  match_id
from match m
inner join tournament t
on t.tournament_id = m.tournament_id
where double = true and m.looser_player_2 is null ;

-- wimbledon,540,2005
