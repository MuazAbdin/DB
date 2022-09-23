create table authors(
        name varchar(50) not null,
        institution varchar(100) not null,
        conference varchar(15) not null,
        count NUMERIC check (count>=1) not null,
        adjustedcount NUMERIC check (adjustedcount>0) not null,
        year integer check (year>0) not null,
        primary key(name,conference,year)
);

create table conferences(
        area varchar(20) not null,
        subarea varchar(20) not null,
        conference varchar(15) primary key
);

create table institutions(
        institution varchar(100) primary key,
        region varchar(20) not null,
        country varchar(2) not null
);
