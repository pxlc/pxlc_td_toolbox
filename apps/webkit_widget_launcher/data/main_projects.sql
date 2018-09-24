CREATE TABLE `Project` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL UNIQUE,
	`description`	TEXT,
	`status`	TEXT NOT NULL
);
CREATE TABLE `Sequence` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL,
	`description`	TEXT,
	`project_id`	INTEGER NOT NULL,
	`status`	TEXT NOT NULL,
    UNIQUE(`code`, `project_id`) ON CONFLICT ROLLBACK
);
CREATE TABLE `Shot` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL,
	`description`	TEXT,
	`project_id`	INTEGER NOT NULL,
	`sequence_id`	INTEGER NOT NULL,
	`status`	TEXT NOT NULL,
    UNIQUE(`code`, `sequence_id`) ON CONFLICT ROLLBACK
);
CREATE TABLE `AssetType` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL,
	`description`	TEXT,
	`project_id`	INTEGER NOT NULL,
    UNIQUE(`code`, `project_id`) ON CONFLICT ROLLBACK
);
CREATE TABLE `Asset` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL,
	`description`	TEXT,
	`project_id`	INTEGER NOT NULL,
	`assettype_id`	INTEGER NOT NULL,
	`status`	TEXT NOT NULL,
    UNIQUE(`code`, `assettype_id`) ON CONFLICT ROLLBACK
);
CREATE TABLE `TaskStep` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL,
	`short_code`	TEXT NOT NULL,
	`description`	TEXT,
	`project_id`	INTEGER NOT NULL,
    UNIQUE(`code`, `project_id`) ON CONFLICT ROLLBACK
);
CREATE TABLE `Task` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL,
	`description`	TEXT,
	`project_id`	INTEGER NOT NULL,
	`taskstep_id`	INTEGER NOT NULL,
    `entity_type`    TEXT,
    `entity_id`    INTEGER,
    `assignees`     TEXT
);

INSERT INTO `Project` (`code`,`description`,`status`)
    VALUES ('thewild','Animated Feature for Disney, called "The Wild"','active');
INSERT INTO `Project` (`code`,`description`,`status`)
    VALUES ('ehero','Animated Film called "Everyone''s Hero"','active');

INSERT INTO `Sequence` (`code`,`description`,`project_id`,`status`)
    VALUES ('q010','Opening credits sequence',1,'in_progress');
-- INSERT INTO `Sequence` (`code`,`description`,`project_id`,`status`)
--     VALUES ('q010','TEST FOR UNIQUE CONSTRAINT',1,'in_progress');
INSERT INTO `Sequence` (`code`,`description`,`project_id`,`status`)
    VALUES ('q020','Beginning of Act I - city zoo intro',1,'in_progress');
INSERT INTO `Sequence` (`code`,`description`,`project_id`,`status`)
    VALUES ('q999','Dev and testing sequence',1,'in_progress');

INSERT INTO `Shot` (`code`,`description`,`project_id`,`sequence_id`,`status`)
    VALUES ('q010s0010','First shot in opening credits',1,1,'in_progress');
-- INSERT INTO `Shot` (`code`,`description`,`project_id`,`sequence_id`,`status`)
--     VALUES ('q010s0010','TEST FOR UNIQUE in Shot table',1,1,'in_progress');
INSERT INTO `Shot` (`code`,`description`,`project_id`,`sequence_id`,`status`)
    VALUES ('q010s0020','Second shot in opening credits',1,1,'in_progress');

INSERT INTO `TaskStep` (`code`,`short_code`,`description`,`project_id`)
    VALUES ('layout','lyo','Layout Task Step',1);
INSERT INTO `TaskStep` (`code`,`short_code`,`description`,`project_id`)
    VALUES ('animation','anm','Animation Task Step',1);
INSERT INTO `TaskStep` (`code`,`short_code`,`description`,`project_id`)
    VALUES ('effects','vfx','Visual Effects Task Step',1);
INSERT INTO `TaskStep` (`code`,`short_code`,`description`,`project_id`)
    VALUES ('light','lgt','Lighting Task Step',1);
INSERT INTO `TaskStep` (`code`,`short_code`,`description`,`project_id`)
    VALUES ('comp','cmp','Compositing Task Step',1);

INSERT INTO `Task` (`code`,`description`,`project_id`,`taskstep_id`,`entity_type`,`entity_id`,`assignees`)
    VALUES ('camera','Layout camera and set task',1,1,'Shot',1,'maquino');

