-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(60) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `aboutMe` VARCHAR(200) NULL,
  `nickname` VARCHAR(45) NOT NULL,
  `joinDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`UserAvatar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`UserAvatar` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `avatarPath` VARCHAR(200) NOT NULL,
  `User_id` INT NOT NULL,
  PRIMARY KEY (`id`, `User_id`),
  INDEX `fk_UserAvatars_User_idx` (`User_id` ASC),
  CONSTRAINT `fk_UserAvatars_User`
    FOREIGN KEY (`User_id`)
    REFERENCES `mydb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `aboutGroup` VARCHAR(200) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`UsersInGroups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`UsersInGroups` (
  `Group_id` INT NOT NULL,
  `User_id` INT NOT NULL,
  `admin` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`Group_id`, `User_id`),
  INDEX `fk_Group_has_User_User1_idx` (`User_id` ASC),
  INDEX `fk_Group_has_User_Group1_idx` (`Group_id` ASC),
  CONSTRAINT `fk_Group_has_User_Group1`
    FOREIGN KEY (`Group_id`)
    REFERENCES `mydb`.`Group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Group_has_User_User1`
    FOREIGN KEY (`User_id`)
    REFERENCES `mydb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`GroupAvatar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GroupAvatar` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Group_id` INT NOT NULL,
  `avatarPath` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`, `Group_id`),
  INDEX `fk_GroupAvatar_Group1_idx` (`Group_id` ASC),
  CONSTRAINT `fk_GroupAvatar_Group1`
    FOREIGN KEY (`Group_id`)
    REFERENCES `mydb`.`Group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Restaurant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Restaurant` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `website` VARCHAR(200) NOT NULL,
  `aboutMe` VARCHAR(200) NULL,
  `joinDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `website_UNIQUE` (`website` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RestaurantAvatar`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`RestaurantAvatar` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `avatarPath` VARCHAR(200) NOT NULL,
  `Restaurants_id` INT NOT NULL,
  PRIMARY KEY (`id`, `Restaurants_id`),
  INDEX `fk_RestaurantAvatar_Restaurants1_idx` (`Restaurants_id` ASC),
  CONSTRAINT `fk_RestaurantAvatar_Restaurants1`
    FOREIGN KEY (`Restaurants_id`)
    REFERENCES `mydb`.`Restaurant` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RestaurantsInGroups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`RestaurantsInGroups` (
  `Restaurants_id` INT NOT NULL,
  `Group_id` INT NOT NULL,
  `rating` FLOAT NOT NULL,
  PRIMARY KEY (`Restaurants_id`, `Group_id`),
  INDEX `fk_Restaurants_has_Group_Group1_idx` (`Group_id` ASC),
  INDEX `fk_Restaurants_has_Group_Restaurants1_idx` (`Restaurants_id` ASC),
  CONSTRAINT `fk_Restaurants_has_Group_Restaurants1`
    FOREIGN KEY (`Restaurants_id`)
    REFERENCES `mydb`.`Restaurant` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Restaurants_has_Group_Group1`
    FOREIGN KEY (`Group_id`)
    REFERENCES `mydb`.`Group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`UserRatings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`UserRatings` (
  `User_id` INT NOT NULL,
  `Restaurant_id` INT NOT NULL,
  `rating` INT(11) NULL,
  `comment` VARCHAR(200) NULL,
  PRIMARY KEY (`User_id`, `Restaurant_id`),
  INDEX `fk_User_has_Restaurant_Restaurant1_idx` (`Restaurant_id` ASC),
  INDEX `fk_User_has_Restaurant_User1_idx` (`User_id` ASC),
  CONSTRAINT `fk_User_has_Restaurant_User1`
    FOREIGN KEY (`User_id`)
    REFERENCES `mydb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Restaurant_Restaurant1`
    FOREIGN KEY (`Restaurant_id`)
    REFERENCES `mydb`.`Restaurant` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
