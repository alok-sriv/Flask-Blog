CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL UNIQUE,
  `email` varchar(100) NOT NULL UNIQUE,
  `image_file` varchar(100) NOT NULL DEFAULT 'default.jpg',
  `password` varchar(100) NOT NULL,
  `register_date` timestamp NOT NULL DEFAULT current_timestamp()
) ;

ALTER TABLE `users` ADD PRIMARY KEY (`id`);
ALTER TABLE `users` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `date_posted` timestamp NOT NULL DEFAULT current_timestamp(),
  `author` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL 
  
) ;

ALTER TABLE `posts` ADD PRIMARY KEY (`id`);
ALTER TABLE `posts` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `posts` ADD FOREIGN KEY (`user_id`) REFERENCES `users`(id);