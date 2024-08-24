-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema excel_file_experiment
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema excel_file_experiment
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `excel_file_experiment` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `excel_file_experiment` ;

-- -----------------------------------------------------
-- Table `excel_file_experiment`.`alembic_version`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `excel_file_experiment`.`alembic_version` ;

CREATE TABLE IF NOT EXISTS `excel_file_experiment`.`alembic_version` (
  `version_num` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`version_num`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `excel_file_experiment`.`author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `excel_file_experiment`.`author` ;

CREATE TABLE IF NOT EXISTS `excel_file_experiment`.`author` (
  `id` INT NOT NULL,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `excel_file_experiment`.`book`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `excel_file_experiment`.`book` ;

CREATE TABLE IF NOT EXISTS `excel_file_experiment`.`book` (
  `id` INT NOT NULL,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `published` TINYINT NULL DEFAULT NULL,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`id`, `author_id`),
  INDEX `fk_book_author_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_book_author`
    FOREIGN KEY (`author_id`)
    REFERENCES `excel_file_experiment`.`author` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
