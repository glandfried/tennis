create table player (
	player_id varchar(4) primary key
	,player_name varchar(32) not null
	-- general 
	,skill float 
	,uncertainty float 
	,last_play date
	,games_played int
	-- hard
	,skill_hard float 
	,uncertainty_hard float
	,last_play_hard date
	,games_played_hard int
	-- clay
	,skill_clay float 
	,uncertainty_clay float 
	,last_play_clay date
	,games_played_clay int
	-- carpet
	,skill_carpet float 
	,uncertainty_carpet float 
	,last_play_carpet date
	,games_played_carpet int
	-- grass
	,skill_grass float
	,uncertainty_grass float 
	,last_play_grass date
	,games_played_grass int
);


--insert into player values ('0000', 'bye', 25, 8.3333, null);

