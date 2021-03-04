CREATE DATABASE IF NOT EXISTS db_name;
CREATE USER 'root'@'%' IDENTIFIED BY 'db_password';
GRANT ALL PRIVILEGES ON db_name.* TO 'root'@'%';