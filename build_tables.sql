DROP TABLE `dbo`.`api_seasons`;

CREATE TABLE `dbo`.`api_seasons`
(
 `id`                INT NOT NULL AUTO_INCREMENT ,
 `api_id`            INT NOT NULL ,
 `start_date`        DATE NOT NULL ,
 `end_date`          DATE NOT NULL ,
 `current_match_day` INT NOT NULL ,

PRIMARY KEY (`id`)
);

INSERT INTO `dbo`.`api_seasons` (api_id, start_date, end_date, current_match_day) VALUES (151, '2018-08-10', '2019-05-12', 1);

DROP TABLE `dbo`.`pickers`;

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

INSERT INTO `dbo`.`pickers` (season_id, team_name, team_short_name, draft_order)
    VALUES
    (1, 'Cole/Raap', 'C/R', 1),
    (1, 'Logan/Ferg', 'L/F', 2),
    (1, 'Trella/Jarrod', 'T/J', 3),
    (1, 'Jeff/Grego', 'J/G', 4);

DROP TABLE `dbo`.`picks`;

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

INSERT INTO `dbo`.`picks` (pickers_id, season_id, team_id, pick_number)
    VALUES
    (1, 1, 6, 1),
    (2, 1, 5, 2),
    (3, 1, 7, 3),
    (4, 1, 9, 4),
    (4, 1, 1, 5),
    (3, 1, 2, 6),
    (2, 1, 3, 7),
    (1, 1, 8, 8),
    (1, 1, 18, 9),
    (2, 1, 12, 10),
    (3, 1, 15, 11),
    (4, 1, 13, 12),
    (4, 1, 10, 13),
    (3, 1, 11, 14),
    (2, 1, 17, 15),
    (1, 1, 4, 16),
    (1, 1, 20, 17),
    (2, 1, 14, 18),
    (3, 1, 16, 19),
    (4, 1, 19, 20);