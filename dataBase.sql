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

COMMIT;
