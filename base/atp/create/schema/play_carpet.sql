create table play_carpet (
	player_id varchar(4) references player(player_id)
	,match_id varchar(18) references match(match_id)
	,skill float
	,uncertainty float
	,skill_old float
	,uncertainty_old float
	,games_played int
	,primary key (player_id, match_id)
);


alter table play_carpet ALTER COLUMN match_id TYPE varchar(20);