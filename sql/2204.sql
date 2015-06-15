begin;
alter table test_profile add column "preview_id" integer REFERENCES "mc_media" ("id") DEFERRABLE INITIALLY DEFERRED;
alter table test_profile add column "preview2_id" integer REFERENCES "mc_media" ("id") DEFERRABLE INITIALLY DEFERRED;
commit;
