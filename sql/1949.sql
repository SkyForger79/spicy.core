begin;
alter table sp_simplepage add column is_deleted boolean default false;
alter table sp_simplepage alter column is_deleted drop default;
--alter table blog_document_site rename to blog_document_sites;
commit;
