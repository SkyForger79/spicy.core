begin;
alter table sp_simplepage add column is_sitemap boolean NOT NULL default 'f';
commit;

