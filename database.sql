drop table if exists sites cascade;
drop table if exists url_check cascade;

CREATE TABLE sites (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name varchar(255) unique not null,
	created_at timestamp not null
);


create table url_check (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	site_id bigint REFERENCES sites (id)
		on delete cascade
		on update set null,
	code_answer integer,
	h1 varchar(255),
	title varchar(255),
	description text,
	created_at timestamp not null
);