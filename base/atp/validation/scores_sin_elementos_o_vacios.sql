select t.tournament_name, m.tournament_id, year, double
from match m
inner join tournament t
on t.tournament_id = m.tournament_id
where m.end_type is null
group by t.tournament_name, m.tournament_id, year, double;

/* 
tournament_name,tournament_id,year,double
london,311,1968,f
montpellier,375,2017,t
barcelona,425,1969,f
monte-carlo,410,1969,f
houston,717,1969,f
atlanta,6116,2015,f
--
london,311,1969,f
paris,352,2001,f
shenzhen,6967,2015,f
australian-open,580,1923,f
australian-open,580,1915,f
australian-open,580,1922,f
monte-carlo,410,1968,f
--
indian-wells,404,1986,f
rome,416,1968,f
barcelona,425,1968,f
gstaad,314,1971,f
kitzbuhel,319,1968,f
kitzbuhel,319,1970,f
sao-paolo,533,2007,f
new-york,424,1972,f
kitzbuhel,319,1997,f
bastad,316,1971,f
*/

