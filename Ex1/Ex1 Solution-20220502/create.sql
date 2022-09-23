create table film(
	id varchar(100) primary key,
	year integer check (year > 0),
	duration integer check (duration>0),
	release_year integer check (release_year > 0),
	title varchar(100) not null,
	studio varchar(100) not null,
	imdb_rating numeric check (imdb_rating >= 0 and imdb_rating <= 10),
	imdb_votes integer check (imdb_votes >= 0),
	content_rating varchar(100) check (content_rating='PG-13' or content_rating='NR' or content_rating='G' or content_rating='PG' or content_rating='R'),
	unique(id, year)
);

create table directed_by(
	film_id varchar(100),
	name varchar(100),
	foreign key(film_id) references film(id),
	primary key(film_id, name)
);

create table written_by(
	film_id varchar(100),
	name varchar(100),
	foreign key(film_id) references film(id),
	primary key(film_id, name)
);

create table acted_by(
	film_id varchar(100),
	name varchar(100),
	foreign key(film_id) references film(id),
	primary key(film_id, name)
);

create table belongs_to(
	film_id varchar(100),
	name varchar(100),
	foreign key(film_id) references film(id),
	primary key(film_id, name)
);

create table won(
	year integer primary key,
	film_id varchar(100),
	foreign key(year, film_id) references film(year, id)
);
