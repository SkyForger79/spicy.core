begin;
alter table sp_simplepage add column is_custom boolean;
update sp_simplepage set is_custom = length(template_name) > 0;
alter table sp_simplepage alter column is_custom set not null;
commit;
