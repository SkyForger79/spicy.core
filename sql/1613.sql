begin;
alter table spicy_settings add column robots text;
UPDATE spicy_settings SET robots = (select robots from seo_chunks);
alter table spicy_settings alter column robots set not null;
commit;
