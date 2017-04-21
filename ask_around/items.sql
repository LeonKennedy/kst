drop table if exists taobao_items;

CREATE TABLE taobao_items(
    id int(34) primary key auto_increment,
    url varchar(255) unique,
    price varchar(55),
    paytimes varchar(25),
    content varchar(255),
    location varchar(55),
    shop_id varchar(55),
    shop_name varchar(55),
    item_id varchar(55) unique,
    category_id int(36),
    tm timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    stat varchar(26) default 'raw',
    foreign key(category_id) references taobao_category(id)
)engine=Innodb default CHARSET=utf8 COMMENT='淘宝商品url';
