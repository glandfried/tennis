create table grouped (
	player_id_1 varchar(4) references player(player_id)
	,player_id_2 varchar(4)  references player(player_id)
	,match_id integer  references match(match_id)
	,sinergia float
	,uncertainty float
	--redundante
	--,sinergia_old float
	--,confidence_old float
	,primary key (player_id_1, player_id_2, match_id)
);

