begin;
alter table sp_simplepage add column is_active boolean NOT NULL default 'f';
alter table sp_simplepage alter column is_active drop default;
commit;
