-- 实例运行环境枚举
drop table if exists instance_env;
create table if not exists instance_env(
    id int not null auto_increment,
    env char(16) not null comment '运行环境',
    env_type tinyint(2) not null comment '环境分类（1：线下环境 2：线上环境）',
    description varchar(128) null comment '备注',
    primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
create unique index env_index on instance_env(env);

-- 实例配置空间枚举
drop table if exists instance_xxf_zone;
create table if not exists instance_xxf_zone(
    id int not null auto_increment,
    zone char(32) not null comment '配置空间',
    description varchar(128) null comment '备注',
    primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
create unique index zone_index on instance_xxf_zone(zone);
