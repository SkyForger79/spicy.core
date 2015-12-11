begin;
alter table spicy_settings add column redmine_tracker_url varchar(255) NOT NULL default '';
alter table spicy_settings add column redmine_username varchar(100) NOT NULL default '';
alter table spicy_settings add column redmine_password varchar(100) NOT NULL default '';
alter table spicy_settings alter column redmine_tracker_url drop default;
alter table spicy_settings alter column redmine_username drop default;
alter table spicy_settings alter column redmine_password drop default;
commit;

