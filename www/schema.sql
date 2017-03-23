-- schema.sql

drop database if exists bugly;

create database bugly;

use bugly;

grant select, insert, update, delete on bugly.* to 'www-data'@'localhost' identified by 'www-data';

CREATE TABLE `users` (
  `id` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `passwd` varchar(50) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `created_at` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`email`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `issues` (
  `id` int(11) NOT NULL,
  `title` varchar(256) NOT NULL,
  `content` mediumtext NOT NULL,
  `content_md5` varchar(50) NOT NULL,
  `version` varchar(32) NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `crashs` (
  `id` varchar(50) NOT NULL,
  `issue_id` int(11) NOT NULL,
  `crash_doc` mediumtext,
  `app_detail` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;