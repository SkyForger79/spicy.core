begin;
alter table test_profile add column "is_ldap_user" boolean NOT NULL default 'f';
alter table test_profile alter column "is_ldap_user" drop default;
commit;