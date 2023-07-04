CREATE TABLE `ai_news` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `summary` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `category` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `source` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `url` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `date_str` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `eth_account` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'account nike name',
  `seed` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'account’s seed phrase ',
  `pri_key` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'account’s private key',
  `address` varchar(128) COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'account’s address',
  `is_on` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'account can be use or not ',
  `balance` decimal(32,0) NOT NULL DEFAULT '0' COMMENT 'account’s eth balance',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_UNIQUE` (`pri_key`),
  UNIQUE KEY `id_UNIQUE` (`id`)
);