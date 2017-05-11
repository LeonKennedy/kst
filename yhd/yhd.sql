drop table if exists yhd_ask;

CREATE TABLE yhd_ask(
    id int(34) primary key auto_increment,
    url varchar(255) ,
    product varchar(255),
    question varchar(1024),
    question_user varchar(55),
    question_tm varchar(36),
    answer varchar(1024),
    answer_user varchar(55) ,
    answer_tm varchar(36),
    tm timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    stat varchar(26) default 'raw'
)engine=Innodb default CHARSET=utf8mb4 COMMENT='一号店问答';
