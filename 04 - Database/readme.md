I am going to use MySQL database, for that I have installed XAMPP (https://www.apachefriends.org/download.html). After installation, you need to type "XAMPP Control Panel" in run of your system to open this. Follow mentioned steps :
1. Start Apache Module from XAMPP
2. Start MySQL Module from XAMPP
3. Click on "Admin" of MySQL module, that will open a browser on your local machine.
4. Click on "Databases" tab and create a new database "flask_blog" for your application.
5. Create require tables.

```sql
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
```
grant all privileges on *.* to root@localhost identified by 'password' with grant option;
pip install flask_mysqldb
pip install passlib
