-- clear script
do $$
declare
  t text;
begin
  for t in
    select table_name
    from information_schema.tables
    where table_schema = 'public'
  loop
    execute 'drop table if exists ' || t || ' cascade';
  end loop;
end $$;

create table DOTS_HISTORY (
  id serial primary key,
  x real not null,
  y real not null,
  r real not null,
  hit boolean not null,
  date varchar(32) not null
);