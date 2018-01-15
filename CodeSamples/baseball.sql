CREATE TABLE `AllStarFullBetter` (
  `playerID` varchar(16) NOT NULL,
  `yearID` int(6) NOT NULL,
  `gameNum` enum('0','1','2') NOT NULL,
  `gameID` char(12) NOT NULL,
  `teamID` char(3) NOT NULL,
  `lgID` enum('NL','AL') NOT NULL,
  `GP` enum('0','1') NOT NULL,
  `startingPos` enum('1','2','3','4','5','6','7','8','9') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


SELECT nameLast, nameFirst FROM Master WHERE nameLast='Williams';