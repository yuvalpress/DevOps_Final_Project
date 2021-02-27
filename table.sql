CREATE TABLE `users_dateTime` (                                                                                                                        `user_id` int(11) NOT NULL,
`user_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
`creation_date` datetime NOT NULL,
PRIMARY KEY (`user_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;