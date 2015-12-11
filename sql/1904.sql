BEGIN;
set constraints all immediate;
ALTER TABLE spicy_siteskin ADD COLUMN home_page_id integer REFERENCES sp_simplepage (id) DEFERRABLE INITIALLY DEFERRED;
COMMIT;


