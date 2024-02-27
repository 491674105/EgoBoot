use projectdb;

drop table if exists project_user_role;
create table if not exists project_user_role
(
    id             bigint      not null auto_increment comment '',
    relative_type  tinyint(2)  not null comment '关系类型（1：与系统/项目的关系 2：与具体服务的关系）',
    system_id      bigint      not null default -1 comment '系统id',
    service_id     bigint      not null default -1 comment '服务id',
    user_info_type tinyint(2)  not null comment '用户信息绑定类型（1：角色信息绑定 2：用户信息绑定）',
    user_id        bigint      not null default -1 comment '用户ID',
    user_name      varchar(64) not null default '-1' comment '员工编号',
    role_id        bigint      not null default -1 comment '用户角色ID',
    del_flag       tinyint(1)  not null default 0 comment '是否删除（1：删除）',
    create_time    datetime    not null default current_timestamp() comment '创建时间',
    update_time    datetime    not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '系统/项目/服务与用户关系表';
create index system_id_index on project_user_role (system_id);
create index service_id_index on project_user_role (service_id);
create index user_id_index on project_user_role (user_id);
create index user_name_index on project_user_role (user_name);
create index role_id_index on project_user_role (role_id);

-- 剔除系统表中人员绑定字段
alter table system_map drop column system_user_id;
alter table system_map drop column deployment_master;
alter table system_map drop column business_line;
alter table system_map drop column pmo;

-- 剔除服务表中人员绑定字段
alter table service drop column business_system;
alter table service drop column service_user_id;
alter table service drop column deployment_master;
alter table service drop column testing_user_id;
alter table service drop column testing_user;
alter table service_info drop column business_system;
alter table service_info drop column service_user_id;
alter table service_info drop column deployment_master;
alter table service_info drop column testing_user_id;
alter table service_info drop column testing_user;

-- 将原有服务与用户关系转移至项目用户数据关系表中
insert into project_user_role(
	relative_type,
	service_id,
	user_info_type,
	user_id
)
select
	2 as 'relative_type',
	service_id,
	2 as 'user_info_type',
	service_user_id as 'user_id'
from service_user
;
-- 重建服务发布参数管理表索引及主键
alter table upload_paramters modify column service_id bigint(20) not null;
create index service_id_index on upload_paramters (service_id);
alter table upload_paramters drop primary key;
alter table upload_paramters add column id bigint(20) not null auto_increment primary key first;

-- 发布日志表添加数据来源字段
alter table publish_log add column publish_source tinyint(2) not null default -1 comment '数据来源' after publish_id;
alter table publish_log add column business_key varchar(64) null default '' comment '数据来源业务键' after publish_source;
update publish_log p
set p.publish_source = 2
where p.publish_id in (
    select * from (
        select
            publish_id
        from publish_log l
        where l.publish_id like 'cmdb%'
    ) base
);

