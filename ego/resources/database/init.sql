SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for archery_ops_log
-- ----------------------------
DROP TABLE IF EXISTS `archery_ops_log`;
CREATE TABLE `archery_ops_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `env` varchar(10) DEFAULT NULL COMMENT '环境CODE',
  `job_id` bigint(20) DEFAULT NULL COMMENT 'JOB ID + task_id 唯一确定运维平台某个工单中的某一个任务',
  `task_id` int(11) DEFAULT NULL COMMENT '任务ID',
  `archery_workflow_ids` varchar(30) DEFAULT NULL COMMENT '对应 archery的 workflow_id，可以有多个，用逗号分隔',
  `stage` varchar(20) DEFAULT NULL COMMENT '阶段：SQL工单分为几个阶段，分别为：SQL检查、SQL提交、SQL审核、SQL执行',
  `status` varchar(20) DEFAULT NULL COMMENT '状态',
  `info` varchar(300) DEFAULT NULL COMMENT '日志详情',
  `create_time` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='archery工单日志';

-- ----------------------------
-- Table structure for archery_task
-- ----------------------------
DROP TABLE IF EXISTS `archery_task`;
CREATE TABLE `archery_task` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `env` varchar(10) NOT NULL COMMENT '环境:dev-开发环境;preprod-预发布环境;hwprod-生产环境',
  `process_id` bigint(20) NOT NULL COMMENT '运维平台JOB ID',
  `task_id` bigint(20) NOT NULL COMMENT '运维平台 TASK ID',
  `se_plan_id` bigint(20) DEFAULT NULL COMMENT '执行计划ID',
  `archery_workflow_id` varchar(50) NOT NULL COMMENT 'archery workflow id',
  `callback_func` varchar(100) DEFAULT NULL COMMENT '执行回调方法',
  `callback_type` varchar(5) DEFAULT NULL COMMENT '发布回调方式，因发布前和发布后回调的是不同的API接口:1-发布前回调;2-发布后回调',
  `status` int(11) DEFAULT NULL COMMENT '''1-正在执行;2-执行成功;3-执行失败''',
  `task_begin_time` datetime DEFAULT NULL COMMENT '任务开始时间',
  `task_end_time` datetime DEFAULT NULL COMMENT '任务结束时间',
  `create_time` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  `mission_no` varchar(64) DEFAULT NULL COMMENT '运维平台 mission_no',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_job_task` (`process_id`,`task_id`,`se_plan_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='运维平台的工单与archery 的工单对应关系';

-- ----------------------------
-- Table structure for ci_task_detail
-- ----------------------------
DROP TABLE IF EXISTS `ci_task_detail`;
CREATE TABLE `ci_task_detail` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` varchar(255) DEFAULT '' COMMENT '业务系统',
  `service` varchar(64) DEFAULT NULL COMMENT '服务名',
  `env` varchar(32) DEFAULT '' COMMENT '发布环境',
  `deploy_tag` varchar(255) DEFAULT '' COMMENT '发布tag',
  `deploy_status` varchar(16) DEFAULT NULL COMMENT '发布状态',
  `deploy_to_server` varchar(255) DEFAULT NULL COMMENT '部署主机',
  `service_port` varchar(6) DEFAULT '' COMMENT '服务端口',
  `deploy_time` datetime DEFAULT NULL COMMENT '发布时间',
  `rollback_tag` varchar(255) DEFAULT NULL,
  `rollback_time` varchar(255) DEFAULT '' COMMENT '回滚时间',
  `mark` varchar(255) DEFAULT '' COMMENT '备注',
  PRIMARY KEY (`task_id`),
  KEY `fk_system` (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for conf_base_info
-- ----------------------------
DROP TABLE IF EXISTS `conf_base_info`;
CREATE TABLE `conf_base_info` (
  `config_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '配置文件唯一id',
  `conf_basename` varchar(255) NOT NULL COMMENT '配置基名',
  `conf_type` varchar(255) NOT NULL COMMENT '配置文件类型',
  `conf_fullname` varchar(255) NOT NULL COMMENT '包含扩展名的配置文件全名',
  `env` varchar(16) NOT NULL,
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `iscommon` bigint(20) NOT NULL COMMENT 'common配置标记为1，非common标记为0',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`config_id`) USING BTREE,
  UNIQUE KEY `uniq_base_info` (`conf_fullname`,`env`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for conf_keys
-- ----------------------------
DROP TABLE IF EXISTS `conf_keys`;
CREATE TABLE `conf_keys` (
  `kid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'key id',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '配置项',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`kid`) USING BTREE,
  UNIQUE KEY `key_index` (`key`) USING BTREE COMMENT '唯一key'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for conf_keys_values_relation
-- ----------------------------
DROP TABLE IF EXISTS `conf_keys_values_relation`;
CREATE TABLE `conf_keys_values_relation` (
  `config_id` bigint(20) NOT NULL COMMENT '配置文件id',
  `kid` bigint(20) NOT NULL COMMENT 'key id',
  `value` varchar(20480) DEFAULT NULL COMMENT '配置项值',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0,
  `mark` varchar(255) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`config_id`,`kid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for conf_permission_associations
-- ----------------------------
DROP TABLE IF EXISTS `conf_permission_associations`;
CREATE TABLE `conf_permission_associations` (
  `pid` bigint(20) NOT NULL AUTO_INCREMENT,
  `kid` bigint(20) NOT NULL COMMENT 'key id',
  `role_id` varchar(20) NOT NULL DEFAULT '-1' COMMENT '角色id',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`pid`) USING BTREE,
  UNIQUE KEY `permission_index` (`role_id`,`kid`) USING BTREE COMMENT '角色和key关联'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for conf_service_info
-- ----------------------------
DROP TABLE IF EXISTS `conf_service_info`;
CREATE TABLE `conf_service_info` (
  `cid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '配置文件id',
  `config_id` bigint(20) NOT NULL COMMENT '配置文件唯一ID',
  `service_id` bigint(20) NOT NULL,
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`cid`) USING BTREE,
  UNIQUE KEY `uniq_index_service_info` (`config_id`,`service_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for conf_softdel_temp
-- ----------------------------
DROP TABLE IF EXISTS `conf_softdel_temp`;
CREATE TABLE `conf_softdel_temp` (
  `kid` bigint(20) NOT NULL,
  `config_id` bigint(20) NOT NULL,
  `del_flag` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`kid`,`config_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for conf_update_temp
-- ----------------------------
DROP TABLE IF EXISTS `conf_update_temp`;
CREATE TABLE `conf_update_temp` (
  `kid` bigint(20) NOT NULL COMMENT '对应key',
  `config_id` bigint(20) NOT NULL COMMENT '对应配置文件',
  `value` varchar(20480) DEFAULT NULL COMMENT '是否删除，1代表删除',
  PRIMARY KEY (`kid`,`config_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for db_hosts
-- ----------------------------
DROP TABLE IF EXISTS `db_hosts`;
CREATE TABLE `db_hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主机ID',
  `ip` char(15) NOT NULL COMMENT '主机IP',
  `vip` varchar(200) DEFAULT NULL COMMENT 'VIP:多个VIP以分号分隔',
  `specs` varchar(255) DEFAULT NULL COMMENT '主机规格',
  `region` enum('重庆总部机房','水土腾龙机房','华为云北京一区可用区1','华为云北京一区可用区2','华为云北京一区可用区3','华为云北京四区可用区1','华为云北京四区可用区2','华为云北京四区可用区3','华为云北京四区可用区7','阿里云') NOT NULL COMMENT '主机区域',
  `type` enum('ECS','RDS','PM','VM') NOT NULL COMMENT '实例载体类型（ECS，RDS，PM：机房物理机，VM：机房虚拟机）',
  `login_type` enum('VNC','RPC','SSH','JUMP','华为云') NOT NULL COMMENT '主机登录方式(VNC,RPC,SSH,JUMP,华为云)',
  `description` varchar(255) DEFAULT NULL COMMENT '主机说明',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='主机';

-- ----------------------------
-- Table structure for db_ins_cluster
-- ----------------------------
DROP TABLE IF EXISTS `db_ins_cluster`;
CREATE TABLE `db_ins_cluster` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '集群ID',
  `name` varchar(255) NOT NULL COMMENT '集群名称',
  `env` int(11) NOT NULL COMMENT '集群环境',
  `type` enum('cluster','master-slave','single') NOT NULL COMMENT '集群类型(cluster,master-slave,single)',
  `db_type` enum('mysql','sqlserver','oracle','mongo') NOT NULL COMMENT '数据库类型（mysql,sqlserver,oracle,mongo）',
  `status` int(11) NOT NULL COMMENT '集群状态（1使用，0未使用）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='数据库集群表';

-- ----------------------------
-- Table structure for db_instance
-- ----------------------------
DROP TABLE IF EXISTS `db_instance`;
CREATE TABLE `db_instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '实例ID',
  `name` varchar(100) NOT NULL COMMENT '实例名',
  `host_id` int(11) NOT NULL COMMENT '实例IP（关联hosts表id）',
  `cluster_id` int(11) DEFAULT NULL COMMENT '实例所属集群（关联cluster表id）',
  `port` int(8) NOT NULL COMMENT '实例端口',
  `status` int(2) NOT NULL COMMENT '实例状态（1使用，0未使用）',
  `role` enum('master','slave','single') NOT NULL COMMENT '实例角色（master，slave，single）',
  `description` varchar(255) DEFAULT NULL COMMENT '说明',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='数据库实例表';

-- ----------------------------
-- Table structure for db_instance_archery_map
-- ----------------------------
DROP TABLE IF EXISTS `db_instance_archery_map`;
CREATE TABLE `db_instance_archery_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `db_instance_id` int(11) DEFAULT NULL COMMENT 'OPS平台中的实例ID',
  `archery_instance_id` int(11) DEFAULT NULL COMMENT 'archery中的实例ID',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='OPS平台与archery中的实例映射';

-- ----------------------------
-- Table structure for db_permissions
-- ----------------------------
DROP TABLE IF EXISTS `db_permissions`;
CREATE TABLE `db_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `name` varchar(255) NOT NULL COMMENT '权限名',
  `level` enum('0','1','2','3','4','5') NOT NULL COMMENT '权限级别（0,1,2,3,4,5）',
  `type` enum('all','mysql','sqlserver','mongodb','oracle','mariadb','cassandra') NOT NULL COMMENT '类型（all,mysql,sqlserver,mongodb,oracle,mariadb,cassandra）',
  `description` varchar(255) DEFAULT NULL COMMENT '说明',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='权限基础表';

-- ----------------------------
-- Table structure for db_schema
-- ----------------------------
DROP TABLE IF EXISTS `db_schema`;
CREATE TABLE `db_schema` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) DEFAULT NULL COMMENT '库名',
  `description` varchar(100) DEFAULT NULL COMMENT '对schema的描述说明',
  `instance_id` int(11) DEFAULT NULL COMMENT '实例ID',
  `create_time` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for db_user_auth
-- ----------------------------
DROP TABLE IF EXISTS `db_user_auth`;
CREATE TABLE `db_user_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户权限ID',
  `user_id` int(11) NOT NULL COMMENT '用户（关联user表id）',
  `schema_id` int(11) NOT NULL COMMENT '授权数据库(关联schema表id)',
  `permissions_id` int(11) NOT NULL COMMENT '用户权限(关联permissions表id)',
  `ua_create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '权限创建时间',
  `ua_update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '权限更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uk_user_schema_privilege` (`user_id`,`schema_id`,`permissions_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='数据库用户权限表';

-- ----------------------------
-- Table structure for db_users
-- ----------------------------
DROP TABLE IF EXISTS `db_users`;
CREATE TABLE `db_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '账户ID',
  `host` varchar(20) DEFAULT NULL COMMENT '允许连接IP段',
  `user` varchar(100) DEFAULT NULL COMMENT '账户名',
  `passwd` varchar(100) DEFAULT NULL COMMENT '账户密码',
  `personal` varchar(255) DEFAULT NULL COMMENT '所属人员',
  `attribute` varchar(10) NOT NULL COMMENT '账户属性("1:应用“，“2:个人")',
  `instance_id` int(11) NOT NULL COMMENT '实例ID',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '账户创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '账户更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='数据库用户表';

-- ----------------------------
-- Table structure for db_users_service
-- ----------------------------
DROP TABLE IF EXISTS `db_users_service`;
CREATE TABLE `db_users_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户服务对应ID',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `service_id` int(11) DEFAULT NULL COMMENT '服务ID',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for front_info
-- ----------------------------
DROP TABLE IF EXISTS `front_info`;
CREATE TABLE `front_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `front_nodes` varchar(128) DEFAULT NULL,
  `front_env` char(16) DEFAULT NULL,
  `build_cmd` varchar(600) DEFAULT NULL,
  `fid` int(255) DEFAULT NULL,
  `cdnurl` varchar(60) DEFAULT NULL,
  `status` tinyint(2) NOT NULL DEFAULT 1 COMMENT '服务实例状态',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_front` (`fid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for gitlab_info
-- ----------------------------
DROP TABLE IF EXISTS `gitlab_info`;
CREATE TABLE `gitlab_info` (
  `project_id` bigint(20) NOT NULL COMMENT 'gitlab项目ID',
  `uri` varchar(255) DEFAULT '' COMMENT 'gitlab仓库地址（SSH版本）',
  `http_uri` varchar(255) DEFAULT '' COMMENT 'gitlab仓库地址（SSH版本）',
  PRIMARY KEY (`project_id`),
  KEY `uri_index` (`uri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for instance_env
-- ----------------------------
DROP TABLE IF EXISTS `instance_env`;
CREATE TABLE `instance_env` (
  id int(11) NOT NULL AUTO_INCREMENT,
  env char(16) NOT NULL COMMENT '运行环境',
  env_type tinyint(2) NOT NULL COMMENT '环境分类（1：线下环境 2：线上环境）',
  simple_code char(2) NOT NULL COMMENT '简码',
  description varchar(128) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `env_index` (`env`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for instance_xxf_zone
-- ----------------------------
DROP TABLE IF EXISTS `instance_xxf_zone`;
CREATE TABLE `instance_xxf_zone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zone` char(32) NOT NULL COMMENT '配置空间',
  `description` varchar(128) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `zone_index` (`zone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for meta_preprod
-- ----------------------------
DROP TABLE IF EXISTS `meta_preprod`;
CREATE TABLE `meta_preprod` (
  `servicename` varchar(255) NOT NULL,
  `healthy_instance` varchar(255) DEFAULT NULL,
  `port` int(255) unsigned DEFAULT NULL,
  `xxf_version` varchar(255) DEFAULT NULL,
  `buildTime` varchar(255) DEFAULT '',
  `xxf_zone` varchar(255) DEFAULT NULL,
  `registerSource` varchar(255) DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for middleware
-- ----------------------------
DROP TABLE IF EXISTS `middleware`;
CREATE TABLE `middleware` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `servicename` varchar(255) NOT NULL,
  `healthy_instance` varchar(255) DEFAULT NULL,
  `port` int(255) unsigned DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL,
  `status` tinyint(2) NOT NULL DEFAULT 0 COMMENT '中间件实例状态',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for nacos_namespace_info
-- ----------------------------
DROP TABLE IF EXISTS `nacos_namespace_info`;
CREATE TABLE `nacos_namespace_info` (
  `id` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `url` varchar(128) DEFAULT '',
  `env` varchar(16) DEFAULT '',
  `namespace` varchar(128) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for object_db
-- ----------------------------
DROP TABLE IF EXISTS `object_db`;
CREATE TABLE `object_db` (
  `db_type` varchar(255) NOT NULL,
  `db_instance` varchar(255) DEFAULT NULL,
  `db_port` int(255) unsigned DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for operate_log
-- ----------------------------
drop table if exists `operate_log`;
create table if not exists `operate_log` (
  `id` bigint not null auto_increment comment '',
  `uri` varchar(255) not null comment '目标路径',
  `endpoint` varchar(255) not null comment '端点',
  `table_name` varchar(128) not null comment '被操作表',
  `op_type` tinyint(1) not null comment '操作类型',
  `host` varchar(255) not null default '127.0.0.1' comment '访问主机',
  `user_id` bigint not null comment '操作人ID',
  `operator` varchar(64) not null comment '操作人',
  `op_time` datetime not null default current_timestamp() comment '操作时间',
  primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '系统操作日志';

-- ----------------------------
-- Table structure for operate_log_detail
-- ----------------------------
drop table if exists `operate_log_detail`;
create table if not exists `operate_log_detail` (
  `id` bigint not null auto_increment comment '',
  `log_id` bigint not null comment '日志ID',
  `description` text not null comment '备注',
  `detail` text not null comment '操作详情（要求使用JSON格式记录）',
  primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '系统操作日志详情';

-- ----------------------------
-- Table structure for ops_config_update_plan
-- ----------------------------
DROP TABLE IF EXISTS `ops_config_update_plan`;
CREATE TABLE `ops_config_update_plan` (
  `cu_plan_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `plan_source` tinyint(2) NOT NULL DEFAULT -1 COMMENT '数据来源',
  `business_key` varchar(64) DEFAULT '' COMMENT '数据来源业务键',
  `task_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '任务ID',
  `cid` bigint(20) NOT NULL COMMENT '配置文件id（配置中心）',
  `config_file` varchar(128) NOT NULL COMMENT '原始配置文件',
  `cache_conf` varchar(128) NOT NULL COMMENT '配置缓存文件（流程中心）',
  `update_status` tinyint(2) NOT NULL COMMENT '配置更新状态',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`cu_plan_id`),
  KEY `task_id_index` (`task_id`),
  KEY `cid_index` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务配置更新计划表';

-- ----------------------------
-- Table structure for ops_process
-- ----------------------------
DROP TABLE IF EXISTS `ops_process`;
CREATE TABLE `ops_process` (
  `process_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '流程ID',
  `process_no` varchar(64) NOT NULL COMMENT '流程编号',
  `process_definition_id` varchar(64) NOT NULL DEFAULT '' COMMENT '流程模板编号',
  `process_instance_id` varchar(64) NOT NULL DEFAULT '' COMMENT '流程实例编号',
  `process_theme` varchar(64) NOT NULL COMMENT '流程主题',
  `originator_id` bigint(20) NOT NULL COMMENT '发起人ID',
  `originator` varchar(64) NOT NULL COMMENT '发起人',
  `process_status` tinyint(2) NOT NULL DEFAULT 1 COMMENT '流程状态',
  `process_type_id` bigint(20) NOT NULL COMMENT '流程类型ID',
  `mark` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`process_id`),
  KEY `process_no_index` (`process_no`),
  KEY `process_instance_id_index` (`process_instance_id`),
  KEY `process_type_id_index` (`process_type_id`),
  KEY `originator_id_index` (`originator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='流程表';

-- ----------------------------
-- Table structure for ops_process_auditors
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_auditors`;
CREATE TABLE `ops_process_auditors` (
  `auditor_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `process_id` bigint(20) NOT NULL COMMENT '流程ID',
  `process_no` varchar(64) NOT NULL COMMENT '流程编号',
  `task_definition_key` varchar(64) NOT NULL COMMENT '任务所属步骤定义KEY',
  `task_definition_name` varchar(128) NOT NULL DEFAULT '' COMMENT '任务所属步骤定义名称',
  `user_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '用户ID',
  `user_name` varchar(64) NOT NULL DEFAULT '' COMMENT '用户名',
  `alias` varchar(64) NOT NULL DEFAULT '' COMMENT '用户别名',
  `role_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '角色ID',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`auditor_id`),
  KEY `process_id_index` (`process_id`),
  KEY `process_no_index` (`process_no`),
  KEY `task_definition_key_index` (`task_definition_key`),
  KEY `user_id_index` (`user_id`),
  KEY `user_name_index` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='发布流程人员关联表';

-- ----------------------------
-- Table structure for ops_process_mission
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_mission`;
CREATE TABLE `ops_process_mission` (
  `mission_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '流程任务ID',
  `mission_no` varchar(64) NOT NULL COMMENT '流程任务编号',
  `parent_mission_no` varchar(64) NOT NULL DEFAULT '' COMMENT '父级任务编号',
  `process_id` bigint(20) NOT NULL COMMENT '流程ID',
  `process_no` varchar(64) NOT NULL COMMENT '流程编号',
  `execution_id` varchar(64) NOT NULL COMMENT '实例执行编号',
  `mission_definition_id` varchar(64) NOT NULL DEFAULT '' COMMENT '任务所属步骤定义ID',
  `mission_definition_key` varchar(64) NOT NULL COMMENT '任务所属步骤定义KEY',
  `mission_definition_name` varchar(128) NOT NULL COMMENT '任务所属步骤定义名称',
  `mission_status` tinyint(2) NOT NULL DEFAULT 1 COMMENT '任务状态',
  `role_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '任务受理人角色ID',
  `user_name` varchar(64) NOT NULL DEFAULT '-1' COMMENT '任务受理人工号',
  `description` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`mission_id`),
  UNIQUE KEY `mission_no_index` (`mission_no`),
  KEY `process_id_index` (`process_id`),
  KEY `process_no_index` (`process_no`),
  KEY `execution_id_index` (`execution_id`),
  KEY `mission_definition_key_index` (`mission_definition_key`),
  KEY `role_id_index` (`role_id`),
  KEY `user_name_index` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='流程任务表';

-- ----------------------------
-- Table structure for ops_process_publish_info
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_publish_info`;
CREATE TABLE `ops_process_publish_info` (
  `info_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '发布类流程详情ID',
  `process_id` bigint(20) NOT NULL COMMENT '流程ID',
  `process_no` varchar(64) NOT NULL COMMENT '流程编号',
  `sys_priority` int(11) NOT NULL DEFAULT 1 COMMENT '任务执行优先级，值越小优先级越高',
  `env` char(16) NOT NULL COMMENT '发布环境',
  `system_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '上线系统ID',
  `business_system` varchar(64) NOT NULL DEFAULT '' COMMENT '上线系统',
  `publish_time` bigint(20) NOT NULL COMMENT '发布计划时间',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`info_id`),
  KEY `process_id_index` (`process_id`),
  KEY `process_no_index` (`process_no`),
  KEY `system_id_index` (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='发布类流程详情表';

-- ----------------------------
-- Table structure for ops_process_publish_role_env
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_publish_role_env`;
CREATE TABLE `ops_process_publish_role_env` (
  `role_env_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `env_type` tinyint(2) DEFAULT NULL COMMENT '环境类型',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`role_env_id`),
  KEY `role_id_index` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='发布流程角色可发布环境类型关系表';

-- ----------------------------
-- Table structure for ops_process_publish_task
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_publish_task`;
CREATE TABLE `ops_process_publish_task` (
  `task_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `task_no` varchar(64) NOT NULL COMMENT '任务编号',
  `process_id` varchar(64) NOT NULL COMMENT '流程ID',
  `process_no` varchar(64) NOT NULL COMMENT '流程编号',
  `task_priority` int(11) NOT NULL DEFAULT 1 COMMENT '任务执行优先级，值越小优先级越高',
  `system_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '上线系统ID',
  `business_system` varchar(64) NOT NULL COMMENT '上线系统',
  `service_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '上线服务ID',
  `service_name` varchar(64) NOT NULL COMMENT '上线服务',
  `service_type` varchar(10) NOT NULL COMMENT '服务类型',
  `publish_method` char(16) NOT NULL COMMENT '发布方式',
  `xxf_zone` char(16) NOT NULL COMMENT '配置空间',
  `publish_tag` varchar(128) NOT NULL COMMENT 'TAG/Branch',
  `status` tinyint(2) NOT NULL COMMENT '发布状态',
  `mark` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`task_id`),
  KEY `task_no_index` (`task_no`),
  KEY `process_id_index` (`process_id`),
  KEY `process_no_index` (`process_no`),
  KEY `system_id_index` (`system_id`),
  KEY `service_id_index` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务发布类型工单任务表';

-- ----------------------------
-- Table structure for ops_process_resources
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_resources`;
CREATE TABLE `ops_process_resources` (
  `resource_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '资源名',
  `process_type` tinyint(2) NOT NULL COMMENT '流程类型',
  `description` varchar(64) DEFAULT NULL COMMENT '资源描述',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`resource_id`),
  KEY `name_index` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='流程资源表';

-- ----------------------------
-- Table structure for ops_process_review
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_review`;
CREATE TABLE `ops_process_review` (
  `review_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `process_id` bigint(20) NOT NULL COMMENT '流程ID',
  `process_no` varchar(64) NOT NULL COMMENT '流程编号',
  `step_id` varchar(64) NOT NULL COMMENT '步骤ID',
  `step_name` varchar(128) NOT NULL DEFAULT '' COMMENT '步骤定义名称',
  `reviewer` varchar(64) NOT NULL COMMENT '审批人',
  `reviewer_id` bigint(20) NOT NULL COMMENT '审批人ID',
  `opinion` tinyint(2) NOT NULL COMMENT '审批意见',
  `reason` varchar(255) DEFAULT '' COMMENT '审批备注',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`review_id`),
  KEY `process_id_index` (`process_id`),
  KEY `process_no_index` (`process_no`),
  KEY `step_id_index` (`step_id`),
  KEY `reviewer_id_index` (`reviewer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='流程审批表';

-- ----------------------------
-- Table structure for ops_process_role_permission
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_role_permission`;
CREATE TABLE `ops_process_role_permission` (
  `permission_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `step_id` varchar(32) NOT NULL COMMENT '步骤ID',
  `resource_id` bigint(20) NOT NULL COMMENT '资源ID',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`permission_id`),
  KEY `role_id_index` (`role_id`),
  KEY `step_id_index` (`step_id`),
  KEY `resource_id_index` (`resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='流程角色权限表';

-- ----------------------------
-- Table structure for ops_process_type
-- ----------------------------
DROP TABLE IF EXISTS `ops_process_type`;
CREATE TABLE `ops_process_type` (
  `type_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(64) NOT NULL COMMENT '类型名',
  `description` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`type_id`),
  KEY `type_name_index` (`type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='流程类型表';

-- ----------------------------
-- Table structure for ops_sql_exec_plan
-- ----------------------------
DROP TABLE IF EXISTS `ops_sql_exec_plan`;
CREATE TABLE `ops_sql_exec_plan` (
  `se_plan_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `plan_source` tinyint(2) NOT NULL DEFAULT -1 COMMENT '数据来源',
  `business_key` varchar(64) DEFAULT '' COMMENT '数据来源业务键',
  `task_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '任务ID',
  `title` varchar(128) NOT NULL COMMENT '执行计划标题',
  `exec_type` tinyint(2) NOT NULL COMMENT '执行方式',
  `exec_time` bigint(20) NOT NULL DEFAULT -1 COMMENT '执行时间',
  `env` char(16) NOT NULL COMMENT '所属环境',
  `instance_id` bigint(20) NOT NULL COMMENT '执行实例ID',
  `exec_inst` varchar(128) NOT NULL COMMENT '执行实例',
  `exec_db_id` bigint(20) NOT NULL COMMENT '执行库ID',
  `exec_db` varchar(128) NOT NULL COMMENT '执行库',
  `exec_sql` varchar(10240) NOT NULL COMMENT 'SQL详情',
  `exec_status` tinyint(2) NOT NULL COMMENT 'SQL执行状态',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`se_plan_id`),
  KEY `task_id_index` (`task_id`),
  KEY `instance_id_index` (`instance_id`),
  KEY `exec_db_id_index` (`exec_db_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SQL执行计划表';

-- ----------------------------
-- Table structure for ports
-- ----------------------------
DROP TABLE IF EXISTS `ports`;
CREATE TABLE `ports` (
  `port` int(11) NOT NULL COMMENT '端口值',
  `type` tinyint(2) NOT NULL COMMENT '端口类型',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '端口状态（0：空闲 1：占用）',
  `reuse` tinyint(1) NOT NULL COMMENT '是否复用（0：否 1：是）',
  PRIMARY KEY (`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for project_user_role
-- ----------------------------
DROP TABLE IF EXISTS `project_user_role`;
CREATE TABLE `project_user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relative_type` tinyint(2) NOT NULL COMMENT '关系类型（1：与系统/项目的关系 2：与具体服务的关系）',
  `system_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '系统id',
  `service_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '服务id',
  `user_info_type` tinyint(2) NOT NULL COMMENT '用户信息绑定类型（1：角色信息绑定 2：用户信息绑定）',
  `user_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '用户ID',
  `user_name` varchar(64) NOT NULL DEFAULT '-1' COMMENT '员工编号',
  `role_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '用户角色ID',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `system_id_index` (`system_id`),
  KEY `service_id_index` (`service_id`),
  KEY `user_id_index` (`user_id`),
  KEY `user_name_index` (`user_name`),
  KEY `role_id_index` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统/项目/服务与用户关系表';

-- ----------------------------
-- Table structure for publish_log
-- ----------------------------
DROP TABLE IF EXISTS `publish_log`;
CREATE TABLE `publish_log` (
  `publish_id` varchar(64) NOT NULL COMMENT '发布记录ID',
  `publish_source` tinyint(2) NOT NULL DEFAULT -1 COMMENT '发布记录数据来源',
  `business_key` varchar(64) DEFAULT '' COMMENT '发布记录数据来源业务键',
  `service_id` bigint(20) NOT NULL COMMENT '服务ID',
  `inst_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '实例ID',
  `publish_subject` tinyint(2) NOT NULL COMMENT '发布主体(0：服务发布 1：单实例发布)',
  `publish_method` char(16) NOT NULL COMMENT '发布方式',
  `env` char(16) NOT NULL COMMENT '发布环境',
  `xxf_zone` char(16) NOT NULL COMMENT '配置空间',
  `publish_tag` varchar(128) NOT NULL COMMENT 'TAG/Branch',
  `commit_id` varchar(64) not null default '' comment 'commit_hash',
  `status` tinyint(2) NOT NULL COMMENT '发布状态',
  `publish_user_id` bigint(20) NOT NULL COMMENT '发布执行人ID',
  `publish_user` varchar(64) NOT NULL COMMENT '发布执行人',
  `publish_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '发布时间',
  `finish_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '完成时间',
  `mark` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`publish_id`),
  KEY `service_id_index` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for registe_service_jar_detail
-- ----------------------------
DROP TABLE IF EXISTS `registe_service_jar_detail`;
CREATE TABLE `registe_service_jar_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `service_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '服务ID',
  `service_name` varchar(64) NOT NULL,
  `healthy_instance` varchar(128) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `env` char(16) DEFAULT NULL,
  `heap_memory` int(11) DEFAULT 512,
  `xxf_zone` char(16) DEFAULT NULL,
  `status` tinyint(2) NOT NULL DEFAULT -1 COMMENT '服务实例状态',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for business_line_info
-- ----------------------------
drop table if exists business_line_info;
create table if not exists business_line_info (
    bl_id bigint not null auto_increment comment '',
    business_line varchar(64) not null comment '',
    del_flag tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
    mark varchar(255) DEFAULT '',
    create_time datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
    update_time datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
    primary key(bl_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '业务线信息';

-- ----------------------------
-- Table structure for system_map
-- ----------------------------
DROP TABLE IF EXISTS `system_map`;
CREATE TABLE `system_map` (
  `system_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `business_system` varchar(255) NOT NULL,
  `bl_id` bigint NOT NULL DEFAULT -1 COMMENT '业务线ID',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `description` varchar(255) DEFAULT '' COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT current_timestamp(),
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '业务系统信息';
-- create unique index `business_system_index` system_map(`business_system`);
create unique index bl_id_sys_idx on system_map(bl_id, business_system);

-- ----------------------------
-- Table structure for service_info
-- ----------------------------
DROP TABLE IF EXISTS `service_info`;
CREATE TABLE `service_info` (
  `service_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(64) NOT NULL,
  `port` int(11) DEFAULT -1,
  `system_id` bigint(20) NOT NULL DEFAULT -1 COMMENT '系统负责人ID',
  `service_type` varchar(10) DEFAULT '',
  `os_type` char(32) NOT NULL DEFAULT 'linux' COMMENT '操作系统类型',
  `build_flag` tinyint(1) NOT NULL DEFAULT 1 COMMENT '编译标识（0：不编译 1：编译）',
  `template` varchar(128) DEFAULT NULL COMMENT '发布模板',
  `flag` tinyint(2) NOT NULL DEFAULT 0 COMMENT '服务标识',
  `status` tinyint(2) NOT NULL DEFAULT 0 COMMENT '服务状态(0：待上线 1：使用中 2：待下线 3：已下线)',
  `publish_flag` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否开启发布功能（0：关闭 1：开启）',
  `mark` varchar(255) DEFAULT '',
  `del_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
  `create_time` datetime NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
  `update_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`service_id`),
  UNIQUE KEY `service_name_index` (`service_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for service_instance
-- ----------------------------
drop table if exists service_instance;
create table if not exists service_instance(
    inst_id bigint not null auto_increment comment '实例ID',
    service_id bigint not null comment '服务ID',
    service_name varchar(64) not null comment '服务名',
    address varchar(128) not null comment '实例地址',
    inst_port int not null comment '实例端口',
    heap_memory int not null default 512 comment '实例堆内存',
    inst_env char(16) not null comment '实例运行环境',
    inst_config_zone char(32) not null default '' comment '实例配置空间',
    build_cmd varchar(1024) not null default '' comment '实例编译命令',
    start_cmd varchar(1024) not null default '' comment '实例启动命令',
    cdn_url varchar(128) null comment '实例CDN地址（仅前端有效）',
    inst_status tinyint(2) not null default -1 comment '服务实例状态',
    del_flag tinyint(1) default 0 not null comment '是否删除（1：删除）',
    create_time datetime default CURRENT_TIMESTAMP not null comment '服务创建时间',
    update_time datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    primary key(inst_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '服务实例信息表';
create index service_id_index on service_instance (service_id);


drop table if exists service_app_scene;
create table if not exists service_app_scene(
  scene_id varchar(64) not null comment '',

  scene_name varchar(255) not null comment '应用场景名称',
  description varchar(255) null comment '描述',

  del_flag tinyint(1) default 0 not null comment '是否删除（1：删除）',
  create_time datetime default CURRENT_TIMESTAMP not null comment '服务创建时间',
  update_time datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
  primary key(scene_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '服务/实例应用场景信息';


drop table if exists service_app_scene_relative;
create table if not exists service_app_scene_relative(
  relative_id varchar(64) not null comment '',

  object_type tinyint(2) not null comment '主体类型',
  object_pk bigint not null comment '主体主键',
  scene_id varchar(64) not null comment '应用场景ID',

  del_flag tinyint(1) default 0 not null comment '是否删除（1：删除）',
  create_time datetime default CURRENT_TIMESTAMP not null comment '服务创建时间',
  update_time datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',

  primary key(relative_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '服务/实例应用场景关联';

-- ----------------------------
-- Table structure for service_git
-- ----------------------------
DROP TABLE IF EXISTS `service_git`;
CREATE TABLE `service_git` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_id` bigint(20) NOT NULL COMMENT 'Gitlab项目ID',
  `uri` varchar(255) DEFAULT '' COMMENT 'Gitlab仓库地址',
  `http_uri` varchar(255) DEFAULT NULL COMMENT 'Gitlab链接（HTTP版）',
  `service_id` bigint(20) NOT NULL COMMENT '服务ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_id` (`service_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for upload_paramters
-- ----------------------------
drop table if exists upload_paramters;
create table upload_paramters (
  id bigint not null auto_increment comment '',
  service_id bigint(20) not null comment '',
  ci_class varchar(255) not null default '' comment 'CI包路径',
  ci_starter varchar(64) not null default '' comment 'CI启动函数',
  cd_class varchar(255) not null default '' comment 'CD包路径',
  cd_starter varchar(64) not null default '' comment 'CD启动函数',
  notice_class varchar(255) not null default '' comment '通知包路径',
  notice_starter varchar(64) not null default '' comment '通知启动函数',
  upload_params varchar(255) not null default '' comment '编译包路径',
  flag tinyint(2) not null default 0 comment '服务标识',
  status tinyint(2) not null default 0 comment '服务状态',
  del_flag tinyint(1) not null default 0 comment '是否删除（1：删除）',
  create_time datetime not null default current_timestamp() comment '服务创建时间',
  update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',
  primary key (id),
  unique key service_id_index (service_id) using BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for website_detail
-- ----------------------------
DROP TABLE IF EXISTS `website_detail`;
CREATE TABLE `website_detail` (
  `servicename` varchar(255) NOT NULL,
  `healthy_instance` varchar(255) DEFAULT NULL,
  `port` int(255) unsigned DEFAULT NULL,
  `xxf_version` varchar(255) DEFAULT NULL,
  `instance` varchar(255) DEFAULT '',
  `env` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table if exists ops_cloud_sync_timestamp;
create table if not exists ops_cloud_sync_timestamp (
    sync_id bigint not null auto_increment comment '',
    sync_tb_name varchar(64) not null comment '',
    cloud_id int not null comment '云ID',
    sync_tp bigint null default -1 comment '',
    primary key(sync_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云信息增量同步时间戳记录';
create unique index sync_tb_name_cid_idx on ops_cloud_sync_timestamp(sync_tb_name, cloud_id);


drop table if exists ops_cloud;
create table if not exists ops_cloud (
    cloud_id bigint not null auto_increment comment '云ID',
    cloud_name varchar(32) not null comment '云名称',

    description varchar(256) null comment '云描述',

    las_sync_time bigint null default -1 comment '最近一次同步时间戳',
    use_admin tinyint(1) not null default 0 comment '是否启用管理服务（1：启动）',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(cloud_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云信息';

drop table if exists ops_cloud_sync_meta_api;
create table if not exists ops_cloud_sync_meta_api (
    api_id bigint not null auto_increment comment '',

    cloud_id int not null comment '云ID',
    uri varchar(256) not null comment '数据接口地址',
    api_method char(16) not null comment '协议方法',
    description varchar(256) not null comment '接口描述',

    primary key(api_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上元数据同步接口列表';


drop table if exists ops_cloud_zone;
create table if not exists ops_cloud_zone (
    zone_id varchar(64) not null comment '云区域ID',
    cloud_id int not null comment '云ID',

    zone_code varchar(64) not null comment '云区域编码',
    simple_code tinyint(2) not null comment '简码',
    zh_cn varchar(128) null default '' comment '云区域名称（中文）',
    en_us varchar(128) null default '' comment '云区域名称（英文）',
    pt_br varchar(128) null default '' comment '云区域名称（葡萄牙语）',
    es_us varchar(128) null default '' comment '云区域名称（美国西班牙语）',
    es_es varchar(128) null default '' comment '云区域名称（西班牙语）',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(zone_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云区域信息';
create unique index cz_idx on ops_cloud_zone(cloud_id, zone_code);

drop table if exists ops_cloud_avl_zone;
create table if not exists ops_cloud_avl_zone (
    az_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    avl_zone_code varchar(64) not null comment '可用区编码',
    avl_zone_status tinyint not null default 0 comment '可用区状态（0：禁用 1：激活）',
    simple_code tinyint(2) not null comment '简码',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(az_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上可用区信息';
create unique index caz_idx on ops_cloud_avl_zone(cloud_id, avl_zone_code);


drop table if exists ops_cloud_corp_project;
create table if not exists ops_cloud_corp_project (
    project_id varchar(64) not null comment '云项目ID',
    cloud_id int not null comment '云ID',
    domain_id varchar(64) null default '' comment '云项目所属帐号ID',
    project_extern_id varchar(64) null default '' comment '云项目ID（云端）',
    project_extern_pid varchar(64) null default '' comment '云项目父级ID（云端）',

    project_code varchar(32) not null comment '云项目编码',
    project_name varchar(64) null default '' comment '云项目名称',
    project_desc varchar(64) null default '' comment '云项目描述',

    project_status tinyint(2) null default 1 comment '云项目状态（1：正常）',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云项目信息';
create index cloud_id_idx on ops_cloud_corp_project(cloud_id);
create index project_code_idx on ops_cloud_corp_project(project_code);
create unique index cp_idx on ops_cloud_corp_project(cloud_id, project_extern_id);


drop table if exists ops_cloud_host_spec;
create table if not exists ops_cloud_host_spec (
    spec_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    spec_extern_id varchar(64) not null comment '规格ID',
    spec_name varchar(64) not null comment '规格名称',
    cpus int not null default 0 comment '云主机物理核心数',
    vcpus int not null default 0 comment '云主机核心数（一般为虚拟核心）',
    ram bigint not null default 0 comment '云主机内存（单位：字节Byte）',
    disk bigint not null default 0 comment '云服务器规格对应要求系统盘大小，当前未使用该参数，缺省值为0',
    swap varchar(32) not null default '' comment '云服务器规格对应要求的交换分区大小，当前未使用该参数，缺省值为空',

    cpu_spec varchar(64) null comment 'cpu规格',
    cpu_architecture varchar(64) null comment 'cpu架构',
    gpu_spec varchar(64) null comment 'gpu规格',
    charge_type char(16) not null comment '计费类型',

    min_bandwidth bigint not null comment '最小带宽（单位：bps）',
    max_bandwidth bigint not null comment '最大带宽（单位：bps）',
    max_pps bigint not null comment '内网最大收发包能力（单位：个）',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime null comment '创建时间',
    update_time datetime null on update current_timestamp() comment '更新时间',

    primary key(spec_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云主机规格信息';
create unique index cse_idx on ops_cloud_host_spec(cloud_id, spec_extern_id);


drop table if exists ops_cloud_zone_host_spec_relative;
create table if not exists ops_cloud_zone_host_spec_relative (
    relative_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    avl_zone_code varchar(64) not null comment '可用区编码',
    spec_extern_id varchar(64) not null comment '规格ID',
    spec_status char(16) not null comment '规格状态',
    az_spec_status char(16) not null comment '可用区规格状态',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime null comment '创建时间',
    update_time datetime null on update current_timestamp() comment '更新时间',

    primary key(relative_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云区域与主机规格关系';
create unique index cazse_idx on ops_cloud_zone_host_spec_relative(cloud_id, avl_zone_code, spec_extern_id);


drop table if exists ops_cloud_class_compare;
create table if not exists ops_cloud_class_compare (
    class_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    class_type char(32) not null comment '状态/类型类别',
    cloud_class char(32) not null default '' comment '云上状态/类型',
    cloud_num_flag tinyint(1) not null default 0 comment '云上真实数据类型是否为数值（0：否 1：是）',
    local_class char(32) not null comment '本地状态/类型',
    local_num_flag tinyint(1) not null default 0 comment '本地真实数据类型是否为数值（0：否 1：是）',

    description varchar(128) null comment '状态描述',
    primary key(class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上状态/类型对照';


drop table if exists ops_cloud_image_type;
create table if not exists ops_cloud_image_type (
    it_id varchar(64) not null comment '镜像类型ID',

    cloud_id int not null comment '云ID',
    image_type char(16) not null comment '镜像类型',
    description varchar(64) not null comment '镜像类型描述',
    has_os_type tinyint(2) not null default 0 comment '是否关联系统类型（1：关联）',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(it_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云镜像分类';


drop table if exists ops_cloud_image_os_type;
create table if not exists ops_cloud_image_os_type (
    ot_id varchar(64) not null comment '系统类型ID',

    cloud_id int not null comment '云ID',
    os_type char(16) not null comment '操作系统类型',
    platform varchar(64) not null comment '操作系统平台',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(ot_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云镜像系统分类';
create unique index cp_idx on ops_cloud_image_os_type(cloud_id, platform);


drop table if exists ops_cloud_image;
create table if not exists ops_cloud_image (
    image_id varchar(64) not null comment '',
    cloud_id int not null comment '云ID',
    image_extern_id varchar(64) not null comment '云镜像ID',
    image_type char(16) not null comment '镜像类型',
    image_name varchar(256) null default '' comment '云镜像名称',
    os_type char(16) not null comment '操作系统类型',
    platform varchar(64) not null comment '操作系统平台',
    os_bit int null default -1 comment '操作系统位数',
    os_version varchar(64) null default '' comment '操作系统版本',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(image_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云镜像信息';
create unique index ci_idx on ops_cloud_image(cloud_id, image_extern_id);


drop table if exists ops_cloud_image_zone_relative;
create table if not exists ops_cloud_image_zone_relative (
    relative_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    image_extern_id varchar(64) not null comment '云镜像ID',
    img_status char(16) not null comment '镜像状态',
    charge_flag tinyint(2) not null default 0 comment '是否收费（1：收费）',

    primary key(relative_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云镜像与区域关系';
create unique index czi_idx on ops_cloud_image_zone_relative(cloud_id, zone_code, image_extern_id);


drop table if exists ops_cloud_volume_type;
create table if not exists ops_cloud_volume_type (
    vt_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    vt_extern_id varchar(64) not null comment '云硬盘规格ID（云端）',
    vt_name varchar(64) not null comment '云硬盘规格（云端）',
    priority int not null default -1 comment '规格优先级（用于排序）',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(vt_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云硬盘类型信息';
create unique index cvt_idx on ops_cloud_volume_type(cloud_id, vt_extern_id);


drop table if exists ops_cloud_vt_zone_relative;
create table if not exists ops_cloud_vt_zone_relative (
    relative_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    vt_extern_id varchar(64) not null comment '云硬盘规格ID（云端）',
    zone_code varchar(64) not null comment '云区域编码',
    avl_zone_code varchar(64) not null comment '可用区编码',

    is_valid tinyint(2) not null default 0 comment '是否可用（1：可用）',
    is_sold_out tinyint(2) not null default 0 comment '售罄标识（1：售罄）',

    primary key(relative_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云硬盘类型与区域关系';
create unique index cvtaz_idx on ops_cloud_vt_zone_relative(cloud_id, vt_extern_id, avl_zone_code);


drop table if exists ops_cloud_host;
create table if not exists ops_cloud_host (
    host_id varchar(64) not null comment '主机ID',
    host_extern_id varchar(64) not null comment '主机ID（云端）',
    host_full_id varchar(64) not null comment '主机ID（云端）',
    host_name varchar(128) not null comment '主机名',
    description varchar(256) null comment '主机描述',
    simple_code tinyint(2) not null default -1 comment '简码',

    spec_id varchar(64) null default '' comment '规格ID',
    img_id varchar(64) null default '' comment '镜像ID',

    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    avl_zone_code varchar(64) not null comment '可用区编码',

    host_state char(32) not null comment '云主机状态',

    launched_time datetime null comment '启动时间',
    terminated_time datetime null comment '关机时间',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(host_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云主机信息';
create index host_extern_id_idx on ops_cloud_host(host_extern_id);
create index cloud_id_idx on ops_cloud_host(cloud_id);
create index zone_code_idx on ops_cloud_host(zone_code);
create unique index ch_idx on ops_cloud_host(cloud_id, host_extern_id);


drop table if exists ops_cloud_host_nc;
create table if not exists ops_cloud_host_nc (
    nc_id varchar(64) not null comment '网卡ID',
    vpc_extern_id varchar(64) not null default '' comment 'VPC_ID（云端）',
    cloud_id int not null comment '云ID',
    host_extern_id varchar(64) not null comment '主机ID（云端）',
    addr4 varchar(32) null default '' comment 'IPv4地址',
    addr6 varchar(64) null default '' comment 'IPv6地址',
    mac varchar(32) null default '' comment 'MAC地址',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(nc_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云网卡信息';
create unique index cm_idx on ops_cloud_host_nc(cloud_id, mac);


drop table if exists ops_cloud_vpc;
create table if not exists ops_cloud_vpc (
    vpc_id varchar(64) not null comment 'VPC_ID',

    vpc_extern_id varchar(64) not null default '' comment 'VPC_ID（云端）',
    vpc_name varchar(64) not null default '' comment 'VPC对应的名称（云端）',
    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',

    network varchar(128) not null default '' comment '网段',
    network_v6 varchar(128) not null default '' comment '网段 IPv6版本',
    vpc_status char(16) not null default '' comment 'VPC状态（云端）',
    description varchar(64) not null default '' comment 'VPC描述信息',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(vpc_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上VPC信息';
create unique index czv_idx on ops_cloud_vpc(cloud_id, zone_code, vpc_extern_id);


drop table if exists ops_cloud_sub_network;
create table if not exists ops_cloud_sub_network (
    sn_id varchar(64) not null comment '',

    sn_extern_id varchar(64) not null default '' comment '子网ID（云端）',
    sn_name varchar(64) not null default '' comment '子网名称（云端）',
    vpc_extern_id varchar(64) not null default '' comment 'VPC_ID（云端）',
    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    avl_zone_code varchar(64) not null comment '可用区编码',

    sub_network varchar(128) not null default '' comment '子网段',
    gateway varchar(32) not null default '' comment '网关',
    sub_network_v6 varchar(128) not null default '' comment '子网段 IPv6版本',
    gateway_v6 varchar(128) not null default '' comment '网关 IPv6版本',
    dhcp tinyint(2) not null default 0 comment '是否开启DHCP（1：开启）',
    dns1 varchar(32) not null default '' comment '',
    dns2 varchar(32) not null default '' comment '',
    sn_status char(16) not null default '' comment '子网状态（云端）',
    description varchar(255) not null default '' comment '子网描述信息',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(sn_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上子网信息';
create unique index cas_idx on ops_cloud_sub_network(cloud_id, avl_zone_code, sn_extern_id);


drop table if exists ops_cloud_safe_group;
create table if not exists ops_cloud_safe_group (
    sg_id varchar(64) not null comment '',

    sg_extern_id varchar(64) not null default '' comment '安全组ID（云端）',
    sg_name varchar(64) not null default '' comment '安全组名称（云端）',
    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    description varchar(255) not null default '' comment '安全组的描述信息',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(sg_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云安全组信息';
create unique index czs_idx on ops_cloud_safe_group(cloud_id, zone_code, sg_extern_id);


drop table if exists ops_cloud_order;
create table if not exists ops_cloud_order (
    order_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    service_type_code varchar(256) not null default '' comment '云服务类型编码',
    service_type_name varchar(256) not null default '' comment '云服务类型名称',
    order_extern_id varchar(64) not null comment '订单ID（云上）',
    order_source tinyint(2) not null default -1 comment '订单来源（云上）',
    order_status tinyint(2) not null default -1 comment '订单状态（云上）',
    order_type tinyint(2) not null default -1 comment '订单类型（云上）',
    contract_id varchar(64) not null default '' comment '合同ID',

    currency_code char(8) not null comment '货币编码',
    unit_code tinyint(2) not null default -1 comment '计量单位',
    order_amount decimal(32,8) not null default 0.0 comment '订单金额（一般为官方产品定价）',
    discounted_price decimal(32,8) not null default 0.0 comment '折后价（实际支付价格）',

    cash_coupon decimal(32,8) not null default 0.0 comment '现金券金额',
    allowance_coupon decimal(32,8) not null default 0.0 comment '代金券金额',
    stored_card_coupon decimal(32,8) not null default 0.0 comment '储值卡金额',
    commission decimal(32,8) not null default 0.0 comment '手续费',
    consumption_coupon decimal(32,8) not null default 0.0 comment '消费金额',

    pay_time datetime null comment '支付时间',

    del_flag tinyint(2) not null default 0 comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上订单信息';


drop table if exists ops_cloud_order_discount;
create table if not exists ops_cloud_order_discount (
    discount_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    order_extern_id varchar(64) not null comment '订单ID（云上）',
    discount_type char(16) not null comment '折扣类型',
    discount_amount decimal(32,8) not null default 0.0 comment '折扣金额',

    primary key(discount_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上订单折扣信息';


drop table if exists ops_cloud_resource_bill;
create table if not exists ops_cloud_resource_bill (
    bill_id varchar(64) not null comment '',

    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    order_extern_id varchar(64) not null default '' comment '订单ID（云上）',
    trade_id varchar(64) not null default '' comment '账单ID（根据云服务逻辑不同，可能生成的来源不同，不作为唯一键使用）',
    currency_code char(8) not null default '' comment '货币编码',
    currency_unit_code tinyint(2) not null default -1 comment '计量单位编码',

    bill_cycle_date date not null default '2018-01-01' comment '账单消费日期',
    bill_type tinyint(2) not null default -1 comment '账单类型',
    period_type tinyint(2) not null default -1 comment '周期类型',
    customer_id varchar(64) not null default '' comment '消费客户ID',

    service_type_code varchar(256) not null default '' comment '云服务类型编码',
    service_type_name varchar(256) not null default '' comment '云服务类型名称',
    resource_type_code varchar(128) not null default '' comment '云资源类型编码',
    resource_type_name varchar(200) not null default '' comment '云资源类型名称',

    resource_id varchar(128) not null default '' comment '资源实例ID',
    resource_name varchar(128) not null default '' comment '资源实例名称',
    sku_code varchar(64) not null default '' comment '资源规格编码',

    usage_type char(24) not null default '' comment '资源使用量类型',
    usages decimal(32,8) not null default 0 comment '资源使用量',
    usage_unit_code tinyint(4) not null default -1 comment '资源使用量计量单位编码',
    package_usage decimal(32,8) not null default 0 comment '套餐资源使用量',
    package_usage_unit_code tinyint(4) not null default -1 comment '套餐资源使用量计量单位编码',
    reserve_usage decimal(32,8) not null default 0 comment '预留资源使用量',
    reserve_usage_unit_code tinyint(4) not null default -1 comment '预留资源使用量计量单位编码',

    charge_mode tinyint(2) not null default -1 comment '计费模式',
    unit_price decimal(32,8) not null default 0 comment '单价',
    price_unit varchar(64) not null default '' comment '单价单位',
    official decimal(32,8) not null default 0 comment '官网价',
    discount decimal(32,8) not null default 0 comment '对应官网价折扣金额',
    amount decimal(32,8) not null default 0 comment '应付金额',
    cash decimal(32,8) not null default 0 comment '现金支付金额',
    credit_limit decimal(32,8) not null default 0 comment '信用额度支付金额',
    allowance_coupon decimal(32,8) not null default 0 comment '代金券支付金额',
    cash_coupon decimal(32,8) not null default 0 comment '现金券支付金额',
    stored_card_coupon decimal(32,8) not null default 0 comment '储值卡支付金额',
    bonus decimal(32,8) not null default 0 comment '奖励金支付金额',
    debt decimal(32,8) not null default 0 comment '欠费金额',
    adjustment decimal(32,8) not null default 0 comment '欠费核销金额',

    product_spec_desc varchar(256) null comment '产品规格描述',

    start_time datetime null comment '账单对应资源使用开始时间',
    end_time datetime null comment '账单对应资源使用结束时间',

    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(bill_id, bill_cycle_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上资源账单信息';


drop table if exists ops_cloud_resource_bill_extra;
create table if not exists ops_cloud_resource_bill_extra (
    bill_id varchar(64) not null comment '资源账单ID',

    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',
    bill_cycle_date date not null default '2018-01-01' comment '账单消费日期',
    resource_tag varchar(1024) not null default 'None' comment '资源标签',
    project_id varchar(128) not null default '-1' comment '项目ID',
    project_name varchar(256) not null default 'None' comment '',
    formula text null comment '实付金额计算公式',

    primary key(bill_id, bill_cycle_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '云上资源账单扩展信息';


drop table if exists ops_jump_res_id_map;
create table if not exists ops_jump_res_id_map (
    map_id varchar(64) not null comment '',
    cmdb_res_node_id varchar(64) not null comment 'CMDB资源节点ID',
    cmdb_res_node_name varchar(64) not null comment 'CMDB资源节点名称',
    cmdb_res_node_type tinyint(2) not null comment 'CMDB资源节点类型',
    jump_assets_node_id varchar(64) not null comment 'jumpserver资源节点ID',
    par_jump_assets_node_id varchar(64) not null comment 'jumpserver父级资源节点ID',
    cloud_id int not null comment '云ID',
    zone_code varchar(64) not null comment '云区域编码',

    del_flag tinyint(2) default 0 not null comment '是否删除（1：删除）',
    create_time datetime not null default current_timestamp() comment '创建时间',
    update_time datetime not null default current_timestamp() on update current_timestamp() comment '更新时间',

    primary key(map_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'jumpserver资源节点ID映射';
