create table match (
	match_id varchar(18) primary key,
	event_id integer not null references event(event_id), 
	round_number int not null,
	round_name varchar(32) not null,
	winner_player_1 varchar(4) not null references player(player_id),
	looser_player_1 varchar(4) not null references player(player_id),
	winner_player_2 varchar(4) references player(player_id),
	looser_player_2 varchar(4) references player(player_id),
	winner_seed varchar(4),	
	looser_seed varchar(4),
	end_type varchar(5)
);


--alter table match add column event_id integer references event(event_id);

/*
update match
set event_id = tournament_id*(10^5)+year*10+(double::int);
*/

/*
select event_id, count(*)
from match
group by event_id;
*/ 

