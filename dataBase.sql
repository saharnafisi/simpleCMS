BEGIN TRANSACTION;
CREATE TABLE "article" (
	`id`	INTEGER,
	`title`	VARCHAR(30),
	`text`	TEXT,
	PRIMARY KEY(`id`)
);
CREATE TABLE "user" (
	`userName`	VARCHAR(30),
	`password`	VARCHAR(30),
	`name`	VARCHAR(50),
	PRIMARY KEY(`userName`)
);
CREATE TABLE `speechs` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`speech`	VARCHAR(200)
	`speaker`   VARCHAR(20)
);

COMMIT;
