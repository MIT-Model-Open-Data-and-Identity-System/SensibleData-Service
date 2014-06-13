USE question_lasse_fb_functional_network;
create table if not exists main (
`id` int(11) not null auto_increment,
`week` int(11) not null,
`timestamp` timestamp not null,
`user_from` varchar(64) not null,
`user_to` varchar(64) not null,
uniqueness_hash binary(20) default null,
primary key (`id`),
unique key `week_to_from` (`week`, `user_to`,`user_from`));
CREATE TABLE researcher LIKE main; 
CREATE TABLE developer LIKE main; 

USE question_lasse_fb_network;
create table if not exists main (
`id` int(11) not null auto_increment,
`week` int(11) not null,
`timestamp` timestamp not null,
`user_from` varchar(64) not null,
`user_to` varchar(64) not null,
uniqueness_hash binary(20) default null,
primary key (`id`),
unique key `week_to_from` (`week`, `user_to`,`user_from`));
CREATE TABLE researcher LIKE main; 
CREATE TABLE developer LIKE main; 

USE question_lasse_bluetooth_network;
create table if not exists main (
`id` int(11) not null auto_increment,
`timestamp` date not null,
`user_from` varchar(64) not null,
`user_to` varchar(64) not null,
`occurrences` int(11) not null default '1',
`latest_timestamp` timestamp not null,
primary key (`id`),
unique key `date_to_from` (`timestamp`, `user_to`,`user_from`));
CREATE TABLE researcher LIKE main; 
CREATE TABLE developer LIKE main; 


