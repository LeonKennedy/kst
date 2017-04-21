drop table if exists taobao_category;

create table taobao_category(
    id int(36) primary key auto_increment,
    name varchar(55) not null,
    url varchar(1025) not null,
    cat varchar(255) unique,
    tm timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    stat varchar(25) default 'raw',
    offset int(12) default 0
)engine=Innodb default CHARSET=utf8 COMMENT='淘宝商品url';


