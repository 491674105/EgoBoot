drop table if exists upload_paramters;
create table if not exists upload_paramters
(
    id              bigint       not null auto_increment comment '',
    `service_id`    bigint(20)   NOT NULL,
    `upload_params` varchar(255) NOT NULL,
    `flag`          tinyint(2)   NOT NULL DEFAULT 0 COMMENT '服务标识',
    `status`        tinyint(2)   NOT NULL DEFAULT 0 COMMENT '服务状态',
    `del_flag`      tinyint(1)   NOT NULL DEFAULT 0 COMMENT '是否删除（1：删除）',
    `create_time`   datetime     NOT NULL DEFAULT current_timestamp() COMMENT '服务创建时间',
    `update_time`   datetime     NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
    PRIMARY KEY (`service_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
create index service_id_index on upload_paramters (service_id);
