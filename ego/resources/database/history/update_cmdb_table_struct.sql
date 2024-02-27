-- 2022-02-17 调整服务信息表结构，以适配CMDB服务

-- 更新业务系统信息表结构
alter table system_map add column system_user_id bigint not null default -1 comment '系统负责人ID';
alter table system_map add column del_flag tinyint(1) not null default 0 comment '是否删除（1：删除）';
alter table system_map add column description varchar(255) null default '' comment '备注';
alter table system_map change description description varchar(255) character set utf8 collate utf8_general_ci default '' null comment '备注' after del_flag;
alter table system_map add column create_time datetime not null default current_timestamp;
alter table system_map add column update_time datetime not null default current_timestamp on update current_timestamp;
-- 添加唯一索引
create unique index business_system_index on system_map(business_system);

-- 备份服务表
create table if not exists service_bak as select * from service;
-- 添加唯一索引
create unique index service_name_index on service(service_name);
-- 新增创建时间、服务标识字段
alter table service add column service_user_id bigint not null default -1 comment '服务负责人ID';
alter table service add column system_id bigint not null default -1 comment '业务系统ID';
alter table service add column create_time datetime not null default current_timestamp comment '服务创建时间';
alter table service add column update_time datetime not null default current_timestamp on update current_timestamp comment '更新时间';
alter table service add column flag tinyint(2) not null default 0 comment '服务标识';
alter table service add column del_flag tinyint(1) not null default 0 comment '是否删除（1：删除）';
alter table service add column status_cache varchar(30) not null comment '状态缓存';
-- 保存原始状态内容
update service set status_cache = status where 1 = 1;
-- 重建状态字段
alter table service drop column status;
alter table service add column status tinyint(2) not null default 0 comment '服务状态';

-- 查询存在CI记录的服务，取第一条发布记录时间为创建时间
create table if not exists service_create_time as 
select 
	s.service_name,
	min(ctd.deploy_time) as create_time
from ci_task_detail ctd 
inner join registe_service_jar_detail rsjd on rsjd.service_name = ctd.service
inner join service s on s.service_name = rsjd.service_name
group by
	s.service_name
;

-- 将获取到的发布时间回写至服务信息
update service s, service_create_time sc 
set s.create_time = sc.create_time
where 
	s.service_name = sc.service_name
;

-- flag=1 不可下线
update service set flag = 1 where status_cache = '不能下线';
-- status=0 待上线
update service set status = 0 where status_cache = '未上线';
-- status=1 使用中
update service set status = 1 where status_cache in ('不能下线','能下线','可以下线','未下线');
-- status=2 待下线
update service set status = 2 where status_cache = '未下线';
-- status=3 已下线
update service set status = 3 where status_cache = '已下线';

-- 删除服务状态缓存字段
alter table service drop column status_cache;

-- 备份实例表
create table if not exists registe_service_jar_detail_bak as select * from registe_service_jar_detail;
-- 新增基础字段
alter table registe_service_jar_detail add column id bigint primary key not null auto_increment;
alter table registe_service_jar_detail add column status tinyint(2) not null default -1 comment '服务实例状态';
alter table registe_service_jar_detail add column del_flag tinyint(1) not null default 0 comment '是否删除（1：删除）';
alter table registe_service_jar_detail add column create_time datetime not null default current_timestamp comment '服务创建时间';
alter table registe_service_jar_detail add column update_time datetime not null default current_timestamp on update current_timestamp comment '更新时间';

-- 添加唯一索引
create unique index instance_index on registe_service_jar_detail(healthy_instance, service_name);
-- 添加外键索引
create index service_id_index on registe_service_jar_detail(service_id);

-- 更新所有实例状态
update registe_service_jar_detail set status = 1 where 1 = 1;
-- 更新实例创建时间、更新时间
update registe_service_jar_detail s, service_create_time sc 
set s.create_time = sc.create_time, s.update_time = sc.create_time
where 
	s.service_name = sc.service_name
;
-- 删除缓存表
drop table if exists service_create_time;

-- 更新中间件信息表结构
alter table middleware add column id bigint primary key not null auto_increment;
alter table middleware add column status tinyint(2) not null default -1 comment '中间件实例状态';
alter table middleware add column del_flag tinyint(1) not null default 0 comment '是否删除（1：删除）';
alter table middleware add column create_time datetime not null default current_timestamp comment '服务创建时间';
alter table middleware add column update_time datetime not null default current_timestamp on update current_timestamp comment '更新时间';
-- 更新所有中间件实例状态
update middleware set status = 1 where 1 = 1;

-- 添加服务测试人员关联
-- alter table service add column testing_user_id bigint not null default -1 comment '测试人员ID';
-- alter table service add column testing_user varchar(64) not null default '' comment '测试人员';
-- alter table service change testing_user_id testing_user_id bigint(20) default -1 not null comment '测试人员ID' after deployment_master;
-- alter table service change testing_user testing_user varchar(64) character set utf8 collate utf8_general_ci default '' not null comment '测试人员' after testing_user_id;

-- 创建服务git仓库关联信息表
drop table if exists service_git;
create table if not exists service_git(
	id bigint not null auto_increment,
	uri varchar(255) null default '' comment 'gitlab仓库地址',
	service_id bigint not null comment '服务ID',

	primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index uri_index on service_git(uri);

-- 添加服务ID
alter table registe_service_jar_detail add column service_id bigint not null default -1 comment '服务ID';
alter table registe_service_jar_detail change service_id service_id bigint(20) default -1 not null comment '服务ID' after id;
-- 补全服务与实例关联信息
update registe_service_jar_detail r, service s
set r.service_id = s.service_id 
where r.service_name = s.service_name;

-- 创建日志记录表
drop table if exists operate_log;
create table if not exists operate_log(
	id bigint not null auto_increment,
	table_name varchar(64) not null comment '被操作表',
	op_type tinyint(1) not null comment '操作类型',
	user_id bigint not null comment '操作人ID',
	operator varchar(64) not null comment '操作人',
	op_time datetime not null default current_timestamp comment '操作时间',
	primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建日志记录详情表
drop table if exists operate_log_detail;
create table if not exists operate_log_detail(
	id bigint not null auto_increment,
	log_id bigint not null comment '日志ID',
	detail text not null comment '操作详情（要求使用JSON格式记录）',
	description text not null default '' comment '备注',
	primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 更新前端实例信息表
alter table front_info add column id bigint primary key not null auto_increment;
alter table front_info add column status tinyint(2) not null default 1 comment '服务实例状态';
alter table front_info add column del_flag tinyint(1) not null default 0 comment '是否删除（1：删除）';
alter table front_info add column create_time datetime not null default current_timestamp comment '服务创建时间';
alter table front_info add column update_time datetime not null default current_timestamp on update current_timestamp comment '更新时间';
-- 添加外键索引
create index service_id_index on front_info(fid);
