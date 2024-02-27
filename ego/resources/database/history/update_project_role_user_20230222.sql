insert into project_user_role(
    relative_type,
    system_id,
    service_id,
    user_info_type,
    role_id
)
select
    2 as 'relative_type',
    -1 as 'system_id',
    si.service_id,
    1 as 'user_info_type',
    9 as 'role_id'
from service_info si
where
    si.del_flag = 0
    and si.service_id not in (
        select
            pur.service_id
        from project_user_role pur
        where
            pur.del_flag = 0
            and pur.relative_type = 2
            and pur.user_info_type = 1
    )
;