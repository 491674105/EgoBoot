select
    if(bli.bl_id is not null, bli.bl_id, -1)            as 'bl_id(业务线ID)',
    if(bli.bl_id is not null, bli.business_line, '')    as 'business_line(业务线)',
    sm.system_id                                        as 'system_id(业务系统ID)',
    sm.business_system                                  as 'business_system(业务系统)',
    s.service_id                                        as 'service_id(服务ID)',
    s.service_name                                      as 'service_name(服务名)',
    s.port                                              as 'port(服务默认端口)',
    si.address_list                                     as 'address_list(地址列表)',
    s.service_type                                      as 'service_type(服务类型编码)',
    if(s.service_type = 'Front', '前端服务', '后端服务')   as 'service_type(服务类型)',
    users.user_list                                     as 'user_list(关联用户ID列表)',
    sg.project_id                                       as 'project_id(Gitlab项目ID)',
    substring(
        sg.uri,
        length(sg.uri) - instr(reverse(sg.uri), '/') + 2,
        (length(sg.uri) - instr(reverse(sg.uri), 'tig.') - 3) - (length(sg.uri) - instr(reverse(sg.uri), '/') + 1)
    )                                                   as 'project_name(Gitlab项目名)',
    substring(
        sg.uri,
        instr(sg.uri, ':') + 1,
        (length(sg.uri) - instr(reverse(sg.uri), '/') + 1) - (instr(sg.uri, ':') + 1)
    )                                                   as 'namespace(Gitlab项目命名空间)',
    sg.http_uri                                         as 'http_uri(HTTP项目链接)',
    sg.uri                                              as 'uri(SSH项目链接)',
    s.mark                                              as 'mark(服务备注)',
    s.create_time                                       as 'create_time(服务创建时间)',
    s.update_time                                       as 'update_time(服务更新时间)'
from service_info s
inner join service_git sg on sg.service_id = s.service_id
inner join system_map sm on sm.system_id = s.system_id
left join business_line_info bli on (bli.del_flag = 0 and bli.bl_id = sm.bl_id)
left join (
    select
        service_id,
        group_concat(
            user_id
            separator '/'
        ) as 'user_list'
    from project_user_role
    where
        del_flag = 0
        and relative_type = 2
        and user_info_type = 2
    group by
        service_id
) users on users.service_id = s.service_id
left join (
    select
        service_id,
        group_concat(
            address
            separator '/'
        ) as 'address_list'
    from service_instance
    where
        del_flag = 0
    group by
        service_id
) si on si.service_id = s.service_id
where
    s.del_flag = 0
    and sm.del_flag = 0
;
