ALTER TABLE `projet_fraudedb`.`transaction_fraude` 
DROP FOREIGN KEY `transaction_fraude_ibfk_1`;
ALTER TABLE `projet_fraudedb`.`transaction_fraude` 
CHANGE COLUMN `typeID` `type` INT NOT NULL AFTER `step`,
CHANGE COLUMN `transactionID` `transactionId` INT NOT NULL ,
CHANGE COLUMN `NameOrig` `nameOrig` VARCHAR(150) NULL DEFAULT NULL ;
ALTER TABLE `projet_fraudedb`.`transaction_fraude` 
ADD CONSTRAINT `transaction_fraude_ibfk_1`
  FOREIGN KEY (`type`)
  REFERENCES `projet_fraudedb`.`typepaiment` (`typeID`);