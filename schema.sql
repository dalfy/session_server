
drop table if exists  sessions;

create table sessions (

  id INTEGER PRIMARY KEY AUTOINCREMENT
  , token TEXT NOT NULL UNIQUE

);

