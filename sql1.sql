DROP TABLE `dbo`.`picks`;


DROP TABLE `dbo`.`pickers`;


DROP TABLE `dbo`.`api_seasons`;


DROP TABLE `dbo`.`api_standings`;


DROP TABLE `dbo`.`api_teams`;



DROP SCHEMA `dbo`;

CREATE SCHEMA `dbo`;


-- ************************************** `dbo`.`api_seasons`

CREATE TABLE `dbo`.`api_seasons`
(
 `id`                INT NOT NULL AUTO_INCREMENT ,
 `api_id`            INT NOT NULL ,
 `start_date`        DATE NOT NULL ,
 `end_date`          DATE NOT NULL ,
 `current_match_day` INT NOT NULL ,

PRIMARY KEY (`id`)
);





-- ************************************** `dbo`.`api_standings`

CREATE TABLE `dbo`.`api_standings`
(
 `id`              INT NOT NULL AUTO_INCREMENT ,
 `team_api_id`     INT NOT NULL ,
 `position`        INT NOT NULL ,
 `played_games`    INT NOT NULL ,
 `won`             INT NOT NULL ,
 `draw`            INT NOT NULL ,
 `lost`            INT NOT NULL ,
 `points`          INT NOT NULL ,
 `goals_for`       INT NOT NULL ,
 `goals_against`   INT NOT NULL ,
 `goal_difference` INT NOT NULL ,

PRIMARY KEY (`id`)
);





-- ************************************** `dbo`.`api_teams`

CREATE TABLE `dbo`.`api_teams`
(
 `id`               INT NOT NULL AUTO_INCREMENT ,
 `api_id`           INT NOT NULL ,
 `area`             VARCHAR(45) ,
 `name`             VARCHAR(45) NOT NULL ,
 `short_name`       VARCHAR(45) NOT NULL ,
 `tla`              VARCHAR(45) ,
 `address`          VARCHAR(90) ,
 `phone`            VARCHAR(45) ,
 `website`          VARCHAR(45) ,
 `email`            VARCHAR(45) ,
 `founded`          INT ,
 `club_colors`      VARCHAR(45) ,
 `venue`            VARCHAR(45) ,
 `api_last_updated` DATETIME NOT NULL ,
 `crest_url`        VARCHAR(250) ,

PRIMARY KEY (`id`)
);





-- ************************************** `dbo`.`pickers`

CREATE TABLE `dbo`.`pickers`
(
 `id`              INT NOT NULL AUTO_INCREMENT ,
 `season_id`       INT NOT NULL ,
 `team_name`       VARCHAR(45) NOT NULL ,
 `team_short_name` VARCHAR(45) NOT NULL ,
 `draft_order`     INT NOT NULL ,

PRIMARY KEY (`id`, `season_id`),
KEY `fkIdx_68` (`season_id`),
CONSTRAINT `FK_68` FOREIGN KEY `fkIdx_68` (`season_id`) REFERENCES `dbo`.`api_seasons` (`id`)
) ENGINE=INNODB;





-- ************************************** `dbo`.`picks`

CREATE TABLE `dbo`.`picks`
(
 `id`          INT NOT NULL AUTO_INCREMENT ,
 `pickers_id`  INT NOT NULL ,
 `season_id`   INT NOT NULL ,
 `team_id`     INT NOT NULL ,
 `pick_number` INT NOT NULL ,

PRIMARY KEY (`id`, `pickers_id`, `season_id`, `team_id`),
KEY `fkIdx_81` (`pickers_id`, `season_id`),
CONSTRAINT `FK_81` FOREIGN KEY `fkIdx_81` (`pickers_id`, `season_id`) REFERENCES `dbo`.`pickers` (`id`, `season_id`),
KEY `fkIdx_86` (`team_id`),
CONSTRAINT `FK_86` FOREIGN KEY `fkIdx_86` (`team_id`) REFERENCES `dbo`.`api_teams` (`id`)
);



INSERT INTO `dbo`.`api_seasons` (api_id, start_date, end_date, current_match_day) VALUES (151, '2018-08-10', '2019-05-12', 2);

INSERT INTO `dbo`.`pickers` (season_id, team_name, team_short_name, draft_order)
    VALUES
    (1, 'Cole/Raap', 'C/R', 1),
    (1, 'Logan/Ferg', 'L/F', 2),
    (1, 'Trella/Jarrod', 'T/J', 3),
    (1, 'Jeff/Grego', 'J/G', 4);