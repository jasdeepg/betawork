drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    owner string not null,
    i int not null,
    timeDay int not null,
    power int not null
);