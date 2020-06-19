create table event_source  (
	event_id integer references event(event_id),
	html varchar,
	primary key (event_id)
);


