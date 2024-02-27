drop table if exists ops_process;
create table if not exists ops_process
(
    process_id            bigint       not null auto_increment comment '流程ID',
    process_no            varchar(64)  not null comment '流程编号',
    process_definition_id varchar(64)  not null default '' comment '流程模板编号',
    process_instance_id   varchar(64)  not null default '' comment '流程实例编号',
    process_theme         varchar(64)  not null comment '流程主题',
    originator_id         bigint       not null comment '发起人ID',
    originator            varchar(64)  not null comment '发起人',
    process_status        tinyint(2)   not null default 1 comment '流程状态',
    process_type_id       bigint       not null comment '流程类型ID',
    mark                  varchar(255) null comment '备注',
    del_flag              tinyint(1)   not null default 0 comment '是否删除（1：删除）',
    create_time           datetime     not null default current_timestamp() comment '创建时间',
    update_time           datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (process_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '流程表';
create index process_no_index on ops_process (process_no);
create index process_instance_id_index on ops_process (process_instance_id);
create index process_type_id_index on ops_process (process_type_id);
create index originator_id_index on ops_process (originator_id);

drop table if exists ops_process_mission;
create table if not exists ops_process_mission
(
    mission_id              bigint       not null auto_increment comment '流程任务ID',
    mission_no              varchar(64)  not null comment '流程任务编号',
    parent_mission_no       varchar(64)  not null default '' comment '父级任务编号',
    process_id              bigint       not null comment '流程ID',
    process_no              varchar(64)  not null comment '流程编号',
    execution_id            varchar(64)  not null comment '实例执行编号',
    mission_definition_id   varchar(64)  not null default '' comment '任务所属步骤定义ID',
    mission_definition_key  varchar(64)  not null comment '任务所属步骤定义KEY',
    mission_definition_name varchar(128) not null comment '任务所属步骤定义名称',
    mission_status          tinyint(2)   not null default 1 comment '任务状态',
    role_id                 bigint       not null default -1 comment '任务受理人角色ID',
    user_name               varchar(64)  not null default '-1' comment '任务受理人工号',
    description             varchar(255) null comment '备注',
    del_flag                tinyint(1)   not null default 0 comment '是否删除（1：删除）',
    create_time             datetime     not null default current_timestamp() comment '创建时间',
    update_time             datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (mission_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '流程任务表';
create unique index mission_no_index on ops_process_mission (mission_no);
create index process_id_index on ops_process_mission (process_id);
create index process_no_index on ops_process_mission (process_no);
create index execution_id_index on ops_process_mission (execution_id);
create index mission_definition_key_index on ops_process_mission (mission_definition_key);
create index role_id_index on ops_process_mission (role_id);
create index user_name_index on ops_process_mission (user_name);


drop table if exists ops_process_type;
create table if not exists ops_process_type
(
    type_id     bigint       not null auto_increment comment '',
    type_name   varchar(64)  not null comment '类型名',
    description varchar(255) null comment '备注',
    del_flag    tinyint(1)   not null default 0 comment '是否删除（1：删除）',
    create_time datetime     not null default current_timestamp() comment '创建时间',
    update_time datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (type_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '流程类型表';
create index type_name_index on ops_process_type (type_name);


drop table if exists ops_process_review;
create table if not exists ops_process_review
(
    review_id   bigint       not null auto_increment comment '',
    process_id  bigint       not null comment '流程ID',
    process_no  varchar(64)  not null comment '流程编号',
    step_id     varchar(64)  not null comment '步骤ID',
    step_name   varchar(128) not null default '' comment '步骤定义名称',
    reviewer    varchar(64)  not null comment '审批人',
    reviewer_id bigint       not null comment '审批人ID',
    opinion     tinyint(2)   not null comment '审批意见',
    reason      varchar(255) null     default '' comment '审批备注',
    create_time datetime     not null default current_timestamp() comment '创建时间',
    update_time datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (review_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '流程审批表';
create index process_id_index on ops_process_review (process_id);
create index process_no_index on ops_process_review (process_no);
create index step_id_index on ops_process_review (step_id);
create index reviewer_id_index on ops_process_review (reviewer_id);


drop table if exists ops_process_auditors;
create table if not exists ops_process_auditors
(
    auditor_id           bigint       not null auto_increment comment '',
    process_id           bigint       not null comment '流程ID',
    process_no           varchar(64)  not null comment '流程编号',
    task_definition_key  varchar(64)  not null comment '任务所属步骤定义KEY',
    task_definition_name varchar(128) not null default '' comment '任务所属步骤定义名称',
    user_id              bigint       not null default -1 comment '用户ID',
    user_name            varchar(64)  not null default '' comment '用户名',
    alias                varchar(64)  not null default '' comment '用户别名',
    role_id              bigint       not null default -1 comment '角色ID',
    del_flag             tinyint(1)   not null default 0 comment '是否删除（1：删除）',
    create_time          datetime     not null default current_timestamp() comment '创建时间',
    update_time          datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (auditor_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '发布流程人员关联表';
create index process_id_index on ops_process_auditors (process_id);
create index process_no_index on ops_process_auditors (process_no);
create index task_definition_key_index on ops_process_auditors (task_definition_key);
create index user_id_index on ops_process_auditors (user_id);
create index user_name_index on ops_process_auditors (user_name);


drop table if exists ops_process_publish_info;
create table if not exists ops_process_publish_info
(
    info_id         bigint      not null auto_increment comment '发布类流程详情ID',
    process_id      bigint      not null comment '流程ID',
    process_no      varchar(64) not null comment '流程编号',
    sys_priority    int         not null default 1 comment '任务执行优先级，值越小优先级越高',
    env             char(16)    not null comment '发布环境',
    system_id       bigint      not null default -1 comment '上线系统ID',
    business_system varchar(64) not null default '' comment '上线系统',
    publish_time    bigint      not null comment '发布计划时间',
    del_flag        tinyint(1)  not null default 0 comment '是否删除（1：删除）',
    create_time     datetime    not null default current_timestamp() comment '创建时间',
    update_time     datetime    not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (info_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '发布类流程详情表';
create index process_id_index on ops_process_publish_info (process_id);
create index process_no_index on ops_process_publish_info (process_no);
create index system_id_index on ops_process_publish_info (system_id);


drop table if exists ops_process_publish_task;
create table if not exists ops_process_publish_task
(
    task_id         bigint       not null auto_increment comment '任务ID',
    task_no         varchar(64)  not null comment '任务编号',
    process_id      varchar(64)  not null comment '流程ID',
    process_no      varchar(64)  not null comment '流程编号',
    task_priority   int          not null default 1 comment '任务执行优先级，值越小优先级越高',
    system_id       bigint       not null default -1 comment '上线系统ID',
    business_system varchar(64)  not null comment '上线系统',
    service_id      bigint       not null default -1 comment '上线服务ID',
    service_name    varchar(64)  not null comment '上线服务',
    service_type    varchar(10)  not null comment '服务类型',
    publish_method  char(16)     not null comment '发布方式',
    xxf_zone        char(16)     not null comment '配置空间',
    publish_tag     varchar(128) not null comment 'TAG/Branch',
    status          tinyint(2)   not null comment '发布状态',
    mark            varchar(255) null comment '备注',
    del_flag        tinyint(1)   not null default 0 comment '是否删除（1：删除）',
    create_time     datetime     not null default current_timestamp() comment '创建时间',
    update_time     datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (task_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '服务发布类型工单任务表';
create index task_no_index on ops_process_publish_task (task_no);
create index process_id_index on ops_process_publish_task (process_id);
create index process_no_index on ops_process_publish_task (process_no);
create index system_id_index on ops_process_publish_task (system_id);
create index service_id_index on ops_process_publish_task (service_id);


drop table if exists ops_config_update_plan;
create table if not exists ops_config_update_plan
(
    cu_plan_id      bigint       not null auto_increment comment '',
    plan_source  tinyint(2)   not null default -1 comment '数据来源',
    business_key    varchar(64)  null default '' comment '数据来源业务键',
    task_id         bigint       not null default -1 comment '任务ID',
    cid             bigint       not null comment '配置文件id（配置中心）',
    config_file     varchar(128) not null comment '原始配置文件',
    cache_conf      varchar(128) not null comment '配置缓存文件（流程中心）',
    update_status   tinyint(2)   not null comment '配置更新状态',
    create_time     datetime     not null default current_timestamp() comment '创建时间',
    update_time     datetime     not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (cu_plan_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '服务配置更新计划表';
create index task_id_index on ops_config_update_plan (task_id);
create index cid_index on ops_config_update_plan (cid);


drop table if exists ops_sql_exec_plan;
create table if not exists ops_sql_exec_plan
(
    se_plan_id      bigint         not null auto_increment comment '',
    plan_source  tinyint(2)     not null default -1 comment '数据来源',
    business_key    varchar(64)    null default '' comment '数据来源业务键',
    task_id         bigint         not null default -1 comment '任务ID',
    title           varchar(128)   not null comment '执行计划标题',
    exec_type       tinyint(2)     not null comment '执行方式',
    exec_time       bigint         not null default -1 comment '执行时间',
    instance_id     bigint         not null comment '执行实例ID',
    exec_inst       varchar(128)   not null comment '执行实例',
    exec_db_id      bigint         not null comment '执行库ID',
    exec_db         varchar(128)   not null comment '执行库',
    exec_sql        varchar(10240) not null comment 'SQL详情',
    exec_status     tinyint(2)     not null comment 'SQL执行状态',
    create_time     datetime       not null default current_timestamp() comment '创建时间',
    update_time     datetime       not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (se_plan_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment 'SQL执行计划表';
create index task_id_index on ops_sql_exec_plan (task_id);
create index instance_id_index on ops_sql_exec_plan (instance_id);
create index exec_db_id_index on ops_sql_exec_plan (exec_db_id);


drop table if exists ops_process_resources;
create table if not exists ops_process_resources
(
    resource_id  bigint      not null auto_increment comment '',
    name         varchar(64) not null comment '资源名',
    process_type tinyint(2)  not null comment '流程类型',
    description  varchar(64) null comment '资源描述',
    del_flag     tinyint(1)  not null default 0 comment '是否删除（1：删除）',
    create_time  datetime    not null default current_timestamp() comment '创建时间',
    update_time  datetime    not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (resource_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '流程资源表';
create index name_index on ops_process_resources (name);


drop table if exists ops_process_role_permission;
create table if not exists ops_process_role_permission
(
    permission_id bigint      not null auto_increment comment '',
    role_id       bigint      not null comment '角色ID',
    step_id       varchar(32) not null comment '步骤ID',
    resource_id   bigint      not null comment '资源ID',
    del_flag      tinyint(1)  not null default 0 comment '是否删除（1：删除）',
    create_time   datetime    not null default current_timestamp() comment '创建时间',
    update_time   datetime    not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (permission_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '流程角色权限表';
create index role_id_index on ops_process_role_permission (role_id);
create index step_id_index on ops_process_role_permission (step_id);
create index resource_id_index on ops_process_role_permission (resource_id);


drop table if exists ops_process_publish_role_env;
create table if not exists ops_process_publish_role_env
(
    role_env_id bigint     not null auto_increment comment '',
    role_id     bigint     not null comment '角色ID',
    env_type    tinyint(2) null comment '环境类型',
    del_flag    tinyint(1) not null default 0 comment '是否删除（1：删除）',
    create_time datetime   not null default current_timestamp() comment '创建时间',
    update_time datetime   not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key (role_env_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 comment '发布流程角色可发布环境类型关系表';
create index role_id_index on ops_process_publish_role_env (role_id);
