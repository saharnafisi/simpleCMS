BEGIN TRANSACTION;
CREATE TABLE "article" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`title`	VARCHAR(30),
	`text`	TEXT
);
COMMIT;
