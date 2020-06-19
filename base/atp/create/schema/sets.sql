create table sets (
	match_id varchar(18) references match (match_id),
	set_number int,
	winner int not null,
	looser int not null,
	primary key (match_id, set_number)
);

