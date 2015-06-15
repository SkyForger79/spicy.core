begin;
alter table spicy_settings add column ga_key varchar(15) not null default '';
alter table spicy_settings alter column ga_key drop default;
commit;
