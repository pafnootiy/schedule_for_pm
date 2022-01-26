BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users_devman" (
	"ID"	INTEGER,
	"name"	TEXT,
	"level"	TEXT,
	"tg_username"	TEXT,
	"discord_username"	TEXT,
	"is_far_east"	INTEGER,
	"time_slot"	TEXT,
	"PM"	TEXT,
	"team_id"	INTEGER
);
COMMIT;
