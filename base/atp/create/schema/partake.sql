create table partake (
	player_id varchar(4) references player(player_id)
	,match_id varchar(18) references match(match_id)
	,won bool not null
	,primary key (player_id, match_id)
);


/*
insert into partake (player_id,match_id, won) 
select *
from (
	select winner_player_1 as player_id, match_id, true as won
	from match
	union
	select looser_player_1 as player_id, match_id, false as won
	from match
	union
	select winner_player_2 as player_id, match_id, true as won
	from match
	union
	select looser_player_2 as player_id, match_id, false as won
	from match
) q
where q.player_id is not null and q.player_id not like '0000'
;
*/


