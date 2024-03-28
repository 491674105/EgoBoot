SET FOREIGN_KEY_CHECKS=0;

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
