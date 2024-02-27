alter table operate_log modify column table_name varchar(128) not null comment '被操作表';
alter table operate_log add column uri varchar(255) not null comment '目标路径' after id;
alter table operate_log add column endpoint varchar(255) not null comment '端点' after uri;
alter table operate_log add column `host` varchar(255) not null default '127.0.0.1' comment '访问主机' after op_type;

alter table operate_log_detail add column description text not null comment '操作描述' after log_id;
alter table operate_log_detail modify column detail text not null comment '操作详情（要求使用JSON格式记录）';

update operate_log_detail ld, operate_log l
set
    ld.description = l.description
where
    ld.log_id = l.id
;

alter table operate_log drop column description;
