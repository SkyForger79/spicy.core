BEGIN;
set constraints all immediate;
ALTER TABLE sp_simplepage ADD COLUMN og_title varchar(255);
ALTER TABLE sp_simplepage ADD COLUMN og_description varchar(255);
ALTER TABLE sp_simplepage ADD COLUMN og_url varchar(255);
ALTER TABLE sp_simplepage ADD COLUMN og_image varchar(255);
COMMIT;
