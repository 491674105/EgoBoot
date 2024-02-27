-- 清空实例元数据
truncate table service_instance;

-- 初始化后端实例数据
insert into service_instance (
    service_id,
    service_name,
    address,
    inst_port,
    heap_memory,
    inst_env,
    inst_config_zone,
    inst_status,
    del_flag,
    create_time,
    update_time
) select
    backend.service_id,
    backend.service_name,
    if(backend.healthy_instance is null, '', backend.healthy_instance) as 'address',
    backend.port                                                       as 'inst_port',
    backend.heap_memory,
    backend.env                                                        as 'inst_env',
    backend.xxf_zone                                                   as 'inst_config_zone',
    backend.status                                                     as 'inst_status',
    backend.del_flag,
    backend.create_time,
    backend.update_time
from registe_service_jar_detail backend
inner join service_info si on backend.service_id = si.service_id
where
    si.service_type = 'Backend'
;


-- 初始化前端实例数据
insert into service_instance (
    service_id,
    service_name,
    address,
    inst_port,
    heap_memory,
    inst_env,
    inst_status,
    build_cmd,
    cdn_url,
    del_flag,
    create_time,
    update_time
) select
    front.fid                                            as 'service_id',
    si.service_name,
    if(front.front_nodes is null, '', front.front_nodes) as 'address',
    443                                                  as 'inst_port',
    0                                                    as 'heap_memory',
    front.front_env                                      as 'inst_env',
    front.status                                         as 'inst_status',
    front.build_cmd                                      as 'build_cmd',
    front.cdnurl                                         as 'cdn_url',
    front.del_flag,
    front.create_time,
    front.update_time
from front_info front
inner join service_info si on front.fid = si.service_id
where
    si.service_type = 'Front'
;