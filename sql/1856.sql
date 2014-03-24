begin;
alter table sp_simplepage add column is_sitemap boolean NOT NULL default 'f';
alter table sp_simplepage alter column is_sitemap drop default;
commit;

