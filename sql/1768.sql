begin;
update sp_simplepage set url = id where url in (select url from sp_simplepage group by url having (count(*)>1));
alter table sp_simplepage ADD UNIQUE (url);
commit;
