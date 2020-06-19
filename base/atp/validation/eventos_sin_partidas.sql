select t.tournament_name, te.tournament_id, te.year,te.double
from tournamentevent te
LEFT JOIN match m
on m.tournament_id = te.tournament_id and m.year = te.year and m.double = te.double
inner join tournament t
on t.tournament_id = te.tournament_id 
where match_id is null;

/*
delray-beach,499,2007,f
buenos-aires,506,2007,f
wimbledon,540,1919,f
wimbledon,540,1920,f
wimbledon,540,1921,f
nitto-atp-finals,605,1972,f
nitto-atp-finals,605,1973,f
nitto-atp-finals,605,1974,f
nitto-atp-finals,605,1975,f
nitto-atp-finals,605,1976,f
nitto-atp-finals,605,1977,f
nitto-atp-finals,605,1978,f
nitto-atp-finals,605,1979,f
nitto-atp-finals,605,1980,f
nitto-atp-finals,605,1981,f
nitto-atp-finals,605,1986,f
nitto-atp-finals,605,1987,f
nitto-atp-finals,605,1988,f
nitto-atp-finals,605,1989,f
nitto-atp-finals,605,1990,f
nitto-atp-finals,605,1991,f
nitto-atp-finals,605,1992,f
nitto-atp-finals,605,1993,f
nitto-atp-finals,605,1994,f
nitto-atp-finals,605,1995,f
nitto-atp-finals,605,1996,f
nitto-atp-finals,605,1997,f
nitto-atp-finals,605,1998,f
nitto-atp-finals,605,1999,f
nitto-atp-finals,605,2000,f
nitto-atp-finals,605,2001,f
nitto-atp-finals,605,2002,f
nitto-atp-finals,605,2003,f
nitto-atp-finals,605,2004,f
nitto-atp-finals,605,2005,f
nitto-atp-finals,605,2006,f
nitto-atp-finals,605,2007,f
nitto-atp-finals,605,2008,f
nitto-atp-finals,605,2009,f
nitto-atp-finals,605,2010,f
nitto-atp-finals,605,2011,f
nitto-atp-finals,605,2012,f
nitto-atp-finals,605,2013,f
nitto-atp-finals,605,2014,f
nitto-atp-finals,605,2015,f
nitto-atp-finals,605,2016,f
nitto-atp-finals,605,2017,f
nitto-atp-finals,605,2003,t
nitto-atp-finals,605,2004,t
nitto-atp-finals,605,2005,t
nitto-atp-finals,605,2006,t
nitto-atp-finals,605,2007,t
nitto-atp-finals,605,2008,t
nitto-atp-finals,605,2009,t
nitto-atp-finals,605,2010,t
nitto-atp-finals,605,2011,t
nitto-atp-finals,605,2012,t
nitto-atp-finals,605,2013,t
nitto-atp-finals,605,2014,t
nitto-atp-finals,605,2015,t
nitto-atp-finals,605,2016,t
nitto-atp-finals,605,2017,t
*/
