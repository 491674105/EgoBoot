-- 手工指定实例信息归属的机房环境
alter table service_instance add cloud_id int not null default 1 comment '云ID/机房ID' after inst_id;

-- 默认归属水土机房
update service_instance
set
    cloud_id = 3
where
    1 = 1
;

-- 预发和生产归属华为云
update service_instance
set
    cloud_id = 2
where
    inst_env in ('preprod', 'hwprod')
;

-- 部署于水土机房的预发和生产服务
update service_instance
set
    cloud_id = 3
where
    inst_env in ('preprod', 'hwprod')
    and inst_id in (
        select
            inst_id
        from service_instance
        where
            cloud_id in (1, 2)
            and inst_env in ('preprod', 'hwprod')
            and (
                address like '172.22%'
                or address like '172.23%'
                or address like '172.24%'
                or address like '172.25%'
                or address like '172.26%'
            )
    )
;