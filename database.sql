drop table if exists urls cascade;
drop table if exists url_checks cascade;

CREATE TABLE urls (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name varchar(255) unique not null,
	created_at date default current_date
);


create table url_checks (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	url_id bigint REFERENCES urls (id)
		on delete cascade
		on update set null,
	status_code integer,
	h1 varchar(255),
	title varchar(255),
	description text,
	created_at date default current_date
);
