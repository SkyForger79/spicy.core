begin;
alter table test_profile add column google_profile_id varchar(100) not null default '';
alter table test_profile alter column google_profile_id drop default;
commit;
