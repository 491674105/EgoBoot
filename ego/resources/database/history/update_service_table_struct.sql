
alter table service_info add column os_type char(32) not null default 'linux' comment '操作系统类型' after service_type;
alter table service_info add column build_flag tinyint(1) not null default 1 comment '编译标识（0：不编译 1：编译）' after os_type;
alter table service_info add column template varchar(128) null comment '发布模板' after build_flag;

update service_info s
set s.service_type = (
	case
		when service_type = 'jar' then 'Backend'
		when service_name = 'cmdb_service' then 'Backend'
		when system_id = 42 then 'Backend'
		else 'Front'
	end
),
s.os_type = 'centos',
s.build_flag = (
	case
		when service_name = 'cmdb_service' then 0
		when system_id = 42 then 0
		else 1
	end

)
where 1 = 1;

-- service_git结构更新
alter table service_git add column project_id bigint not null comment 'Gitlab项目ID' after id;
alter table service_git add column http_uri varchar(255) null comment 'Gitlab链接（HTTP版）' after uri;

-- 创建gitlab信息表
drop table if exists gitlab_info;
create table if not exists gitlab_info(
	project_id bigint not null comment 'gitlab项目ID',
	uri varchar(255) null default '' comment 'gitlab仓库地址（SSH版本）',
	http_uri varchar(255) null default '' comment 'gitlab仓库地址（SSH版本）',

	primary key(project_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index uri_index on gitlab_info(uri);
-- 清空gitlab数据表
truncate table gitlab_info;
-- 更新服务元数据
update service_git sg, gitlab_info gi
set sg.project_id = gi.project_id, sg.http_uri = gi.http_uri
where sg.uri = gi.uri;

-- 发布记录
drop table if exists publish_log;
create table if not exists publish_log (
	publish_id varchar(64) not null comment '发布记录ID',
	service_id bigint not null comment '服务ID',
	publish_subject tinyint(2) not null comment '发布主体(0：服务发布 1：单实例发布)',
	publish_method char(16) not null comment '发布方式',
 	env char(16) not null comment '发布环境',
	xxf_zone char(16) not null comment '配置空间',
	publish_tag varchar(128) not null comment 'TAG/Branch',
	status tinyint(2) not null comment '发布状态',
	publish_user_id bigint not null comment '发布执行人ID',
	publish_user varchar(64) not null comment '发布执行人',
	publish_time datetime not null default current_timestamp comment '发布时间',
	finish_time datetime not null default current_timestamp on update current_timestamp comment '完成时间',
	mark varchar(255) null comment '备注',

	primary key(publish_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index service_id_index on publish_log(service_id);
