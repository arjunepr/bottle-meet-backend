CREATE TABLE `users` (
  `id` INT unsigned NOT NULL AUTO_INCREMENT COMMENT 'Id for each user',
  `username` VARCHAR(55) NOT NULL,
  `password` BINARY(59) NOT NULL
);
