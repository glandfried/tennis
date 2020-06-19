create table event (
	event_id integer primary key,	
	tour_id int references tournament(tour_id),
	year int not null,
	double bool not null,
	challenger bool not null,
	time_start date not null ,
	time_end date,
	ground varchar(16)
);



/*
insert into event
select tournament_id * (10^5) + year * (10) + double::int as event_id
, tournament_id 
, year
, double
, time_start
, time_end
from tournamentevent;
*/
