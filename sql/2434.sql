begin;
alter table test_profile add column sms_notification boolean default false;
alter table test_profile add column skype varchar(40) not null default '';
alter table test_profile add column inner_phone varchar(100) not null default '';
alter table test_profile add column sendmail_since TIMESTAMP;
alter table test_profile add column sendmail_for TIMESTAMP;
alter table test_profile add column sip_account varchar(150);
commit;

