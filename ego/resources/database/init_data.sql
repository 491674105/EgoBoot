-- 实例运行环境枚举
truncate table instance_env;
insert into instance_env(env, env_type, simple_code)
values ('dev', 1, '01'),
       ('test', 1, '02'),
       ('test-large', 1, '03'),
       ('preprod', 2, '04'),
       ('hwprod', 2, '05')
;


-- 实例配置空间枚举
truncate table instance_xxf_zone;
insert into instance_xxf_zone(zone)
values ('default-normal'),
       ('default-grey'),
       ('beta-normal'),
       ('beta-grey')
;


-- 工单类型
truncate table ops_process_type;
insert into ops_process_type (type_name, description)
values ('Publish', '发布类'),
       ('ConfigChange', '配置变更类')
;


-- 工单表单资源
truncate table ops_process_resources;
insert into ops_process_resources (resource_id, name, process_type, description)
values (1, 'publish_select_env', 1, '发布环境'),
       (2, 'publish_input_process_theme', 1, '工单主题'),
       (3, 'publish_table_publish_plan', 1, '发布计划'),
       (4, 'publish_table_work_order_tasks', 1, '工单任务'),
       (5, 'publish_radio_opinion', 1, '审批意见'),
       (6, 'publish_input_reason', 1, '审批备注'),
       (7, 'publish_textarea_mark', 1, '备注'),
       (8, 'publish_select_auditors', 1, '相关人员'),
       (9, 'publish_btn_temp_storage', 1, '暂存'),
       (10, 'publish_btn_move', 1, '流转'),
       (11, 'publish_btn_send_back', 1, '退回')
;


-- 工单资源与角色关联
truncate table ops_process_role_permission;
insert into ops_process_role_permission (role_id, step_id, resource_id)
values
-- 项目经理（线上发起）
(24, 'p1', 1),
(24, 'p1', 2),
(24, 'p1', 3),
(24, 'p1', 7),
(24, 'p1', 8),
(24, 'p1', 9),
(24, 'p1', 10),

-- 开发人员（线下发起）
(25, 'p1', 1),
(25, 'p1', 2),
(25, 'p1', 3),
(25, 'p1', 7),
(25, 'p1', 8),
(25, 'p1', 10),
(25, 'p1', 11),

-- 开发人员（初始化）
(25, 'p2', 1),
(25, 'p2', 2),
(25, 'p2', 3),
(25, 'p2', 4),
(25, 'p2', 7),
(25, 'p2', 8),
(25, 'p2', 10),

-- 项目开发组长（线上审批）
(17, 'p3', 1),
(17, 'p3', 2),
(17, 'p3', 3),
(17, 'p3', 4),
(17, 'p3', 5),
(17, 'p3', 6),
(17, 'p3', 7),
(17, 'p3', 10),
(17, 'p3', 11),

-- 项目管理部总监（线上审批）
(16, 'p4', 1),
(16, 'p4', 2),
(16, 'p4', 3),
(16, 'p4', 4),
(16, 'p4', 5),
(16, 'p4', 6),
(16, 'p4', 7),
(16, 'p4', 10),
(16, 'p4', 11),

-- 项目开发部总监（线上审批）
(18, 'p5', 1),
(18, 'p5', 2),
(18, 'p5', 3),
(18, 'p5', 4),
(18, 'p5', 5),
(18, 'p5', 6),
(18, 'p5', 7),
(18, 'p5', 10),
(18, 'p5', 11),

-- 技术研发部总监（线上审批）
(19, 'p6', 1),
(19, 'p6', 2),
(19, 'p6', 3),
(19, 'p6', 4),
(19, 'p6', 5),
(19, 'p6', 6),
(19, 'p6', 7),
(19, 'p6', 10),
(19, 'p6', 11),

-- 数据库运维（线上审批）
(7, 'p71', 1),
(7, 'p71', 2),
(7, 'p71', 3),
(7, 'p71', 4),
(7, 'p71', 5),
(7, 'p71', 6),
(7, 'p71', 7),
(7, 'p71', 10),
(7, 'p71', 11),

-- 系统运维（线上审批）
(4, 'p72', 1),
(4, 'p72', 2),
(4, 'p72', 3),
(4, 'p72', 4),
(4, 'p72', 5),
(4, 'p72', 6),
(4, 'p72', 7),
(4, 'p72', 10),
(4, 'p72', 11),

-- 信息运维部经理（线上审批）
(20, 'p8', 1),
(20, 'p8', 2),
(20, 'p8', 3),
(20, 'p8', 4),
(20, 'p8', 5),
(20, 'p8', 6),
(20, 'p8', 7),
(20, 'p8', 10),
(20, 'p8', 11),

-- 测试工程师（线上测试验收）
(9, 'p10', 1),
(9, 'p10', 2),
(9, 'p10', 3),
(9, 'p10', 4),
(9, 'p10', 5),
(9, 'p10', 6),
(9, 'p10', 7),
(9, 'p10', 10),
(9, 'p10', 11),

-- 产品经理（线上产品验收）
(21, 'p11', 1),
(21, 'p11', 2),
(21, 'p11', 3),
(21, 'p11', 4),
(21, 'p11', 5),
(21, 'p11', 6),
(21, 'p11', 7),
(21, 'p11', 10),
(21, 'p11', 11),

-- 项目经理（线上项目验收）
(15, 'p12', 1),
(15, 'p12', 2),
(15, 'p12', 3),
(15, 'p12', 4),
(15, 'p12', 5),
(15, 'p12', 6),
(15, 'p12', 7),
(15, 'p12', 10),
(15, 'p12', 11)
;


-- 发布工单环境角色关联
truncate table ops_process_publish_role_env;
insert into ops_process_publish_role_env (role_id, env_type)
values
-- 工单发布角色（线上）
(24, 2),
-- 开发角色（线下）
(25, 1),
-- 运维角色
(4, 1),
(4, 2),
(7, 1),
(7, 2)
;


-- 业务线信息初始化
truncate table business_line_info;
insert into business_line_info (bl_id, business_line)
values (1, '互联网业务'),
       (2, '线下零售业务'),
       (3, '物流业务'),
       (4, '大宗业务线'),
       (5, '中台业务线'),
       (6, '大数据业务线'),
       (7, '安全业务线'),
       (8, '中间件业务线'),
       (9, '基础业务线'),
       (10, '财务业务线')
;


-- 服务/实例应用场景信息初始化
truncate table service_app_scene;
insert into service_app_scene (scene_id, scene_name)
values ('001', '通用场景'),
       ('4c1e8fb4-7fa3-5d1b-ba00-62640ed994ec', '场景一'),
       ('f8a32c41-f811-5358-9498-012061f5e554', '场景二'),
       ('7fb0e008-3c47-53c0-857d-994f8d5cdc2f', '场景三'),
       ('a5ecf880-c1f8-5301-ad48-7a4028b31bc3', '场景四'),
       ('2664458c-aa00-5a95-b2cb-6f864703ae2d', '场景五'),
       ('853de783-a740-5266-82e0-0f5754e85c13', '场景六'),
       ('06406167-eac8-5443-b46d-d55bd42755c1', '场景七'),
       ('2d0e2677-611e-5ae1-bedf-2ac2891c76ab', '场景八'),
       ('9281f5e3-a9fc-52ff-acd4-b601c748c7f6', '场景九')
;

-- 服务/实例应用场景信息关联初始化
insert into service_app_scene_relative( relative_id, object_type, object_pk, scene_id)
select
    UUID() as 'relative_id',
    2 as object_type,
    service_id as object_pk,
    '001' as 'scene_id'
from service_info
where
    del_flag = 0
;

-- 云信息初始化
truncate table ops_cloud;
insert into ops_cloud (cloud_id, cloud_name, description, use_admin)
values (1, 'DefaultCloud', '云服务（默认）', 0),
       (2, 'HuaweiCloud', '华为云', 1),
       (3, 'CQShuiTuCloud', '重庆水土云机房', 0)
;


-- 云上元数据同步接口列表初始化
truncate table ops_cloud_sync_meta_api;
insert into ops_cloud_sync_meta_api (cloud_id, uri, api_method, description)
values (2, '/cmdbapi/register/warrant/cec/v1/scz', 'post', '同步云上区域信息'),
       (2, '/cmdbapi/register/warrant/cec/v1/scaz', 'post', '同步云上可用区信息'),
       (2, '/cmdbapi/register/warrant/cec/v1/sccp', 'post', '同步云上项目信息'),
       (2, '/cmdbapi/register/warrant/cec/v1/sces', 'post', '同步云主机规格详情列表'),
       (2, '/cmdbapi/register/warrant/cec/v1/sci', 'post', '同步云上镜像列表'),
       (2, '/cmdbapi/register/warrant/cec/v1/sce', 'post', '同步云主机元数据'),
       (2, '/cmdbapi/register/warrant/cec/v1/scv', 'post', '同步云上VPC信息'),
       (2, '/cmdbapi/register/warrant/cec/v1/scsn', 'post', '同步云上子网信息'),
       (2, '/cmdbapi/register/warrant/cec/v1/scsg', 'post', '同步云上安全组信息'),
       (2, '/cmdbapi/register/warrant/cec/v1/scol', 'post', '同步云上订单列表'),
       (2, '/cmdbapi/register/warrant/cec/v1/scrbl', 'post', '同步云上资源账单列表')
;


-- 云上状态/类型对照信息初始化
truncate table ops_cloud_class_compare;
insert into ops_cloud_class_compare (
    class_id, cloud_id, class_type, cloud_class, cloud_num_flag, local_class, local_num_flag, description
)
-- 华为云
       -- 计费场景
values (uuid(), 2, 'charge_scene', 'prePaid', 0, 'period', 0, '预付费（包年/包月）'),
       (uuid(), 2, 'charge_scene', 'postPaid', 0, 'demand', 0, '后付费（按需计费）'),
       -- 计费类型
       (uuid(), 2, 'charge_mode', '1', 1, 'period', 0, '包年/包月'),
       (uuid(), 2, 'charge_mode', '3', 1, 'demand', 0, '按需'),
       (uuid(), 2, 'charge_mode', '10', 1, 'reserved_instances', 0, '预留实例'),
       (uuid(), 2, 'charge_mode', '11', 1, 'savings_plan', 0, '节省计划'),
       -- 周期类型
       (uuid(), 2, 'period_type', '19', 1, 'year', 0, '年'),
       (uuid(), 2, 'period_type', '20', 1, 'month', 0, '月'),
       (uuid(), 2, 'period_type', '24', 1, 'day', 0, '天'),
       (uuid(), 2, 'period_type', '25', 1, 'hour', 0, '小时'),
       (uuid(), 2, 'period_type', '5', 1, 'once', 0, '一次性'),
       -- 云主机规格状态
       (uuid(), 2, 'host_spec_status', 'normal', 0, 'normal', 0, '正常商用'),
       (uuid(), 2, 'host_spec_status', 'abandon', 0, 'deactivate', 0, '下线（即不显示）'),
       (uuid(), 2, 'host_spec_status', 'sellout', 0, 'sellout', 0, '售罄'),
       (uuid(), 2, 'host_spec_status', 'obt', 0, 'open_beta', 0, '公测'),
       (uuid(), 2, 'host_spec_status', 'obt_sellout', 0, 'open_beta_sellout', 0, '公测售罄'),
       (uuid(), 2, 'host_spec_status', 'promotion', 0, 'promotion', 0, '推荐(等同normal，也是商用)'),
       -- 云镜像状态
       (uuid(), 2, 'image_status', 'queued', 0, 'init', 0, '表示镜像元数据已经创建成功，等待上传镜像文件。'),
       (uuid(), 2, 'image_status', 'saving', 0, 'upload', 0, '表示镜像正在上传文件到后端存储。'),
       (uuid(), 2, 'image_status', 'deleted', 0, 'deleted', 0, '表示镜像已经删除。'),
       (uuid(), 2, 'image_status', 'killed', 0, 'error', 0, '表示镜像上传错误。'),
       (uuid(), 2, 'image_status', 'active', 0, 'active', 0, '表示镜像可以正常使用。'),
       -- 云主机状态
       (uuid(), 2, 'host_status', 'build', 0, 'build', 0, '创建实例后，在实例状态进入运行中之前的状态。'),
       (uuid(), 2, 'host_status', 'reboot', 0, 'reboot', 0, '实例正在进行重启操作。'),
       (uuid(), 2, 'host_status', 'hard_reboot', 0, 'hard_reboot', 0, '实例正在进行强制重启操作。'),
       (uuid(), 2, 'host_status', 'rebuild', 0, 'rebuild', 0, '实例正在重建中。'),
       (uuid(), 2, 'host_status', 'migrating', 0, 'migrating', 0, '实例正在热迁移中。'),
       (uuid(), 2, 'host_status', 'resize', 0, 'resize', 0, '实例接收变更请求，开始进行变更操作。'),
       (uuid(), 2, 'host_status', 'active', 0, 'active', 0, '实例正常运行状态。'),
       (uuid(), 2, 'host_status', 'shutoff', 0, 'shutdown', 0, '实例被正常停止。'),
       (uuid(), 2, 'host_status', 'revert_resize', 0, 'revert_resize', 0, '实例正在回退变更规格的配置。'),
       (uuid(), 2, 'host_status', 'verify_resize', 0, 'verify_resize', 0, '实例正在校验变更完成后的配置。'),
       (uuid(), 2, 'host_status', 'error', 0, 'error', 0, '实例处于异常状态。'),
       (uuid(), 2, 'host_status', 'deleted', 0, 'deleted', 0, '实例已被正常删除。'),
       (uuid(), 2, 'host_status', 'shelved', 0, 'shelved', 0, '镜像启动的实例处于搁置状态。'),
       (uuid(), 2, 'host_status', 'shelved_offloaded', 0, 'shelved_offloaded', 0, '卷启动的实例处于搁置状态。'),
       (uuid(), 2, 'host_status', 'unknown', 0, 'unknown', 0, '实例处于未知状态。'),
       -- 金额计量单位
       (uuid(), 2, 'unit_code', '1', 1, '1', 1, '元'),
       -- 云订单类型
       (uuid(), 2, 'order_type', '1', 1, '1', 1, '开通'),
       (uuid(), 2, 'order_type', '2', 1, '2', 1, '续订'),
       (uuid(), 2, 'order_type', '3', 1, '3', 1, '变更'),
       (uuid(), 2, 'order_type', '4', 1, '4', 1, '退订'),
       (uuid(), 2, 'order_type', '10', 1, '10', 1, '包年/包月转按需'),
       (uuid(), 2, 'order_type', '11', 1, '11', 1, '按需转包年/包月'),
       (uuid(), 2, 'order_type', '13', 1, '13', 1, '试用'),
       (uuid(), 2, 'order_type', '14', 1, '14', 1, '转商用'),
       (uuid(), 2, 'order_type', '15', 1, '15', 1, '费用调整'),
       -- 云订单来源
       (uuid(), 2, 'order_source_type', '1', 1, '1', 1, '客户'),
       (uuid(), 2, 'order_source_type', '2', 1, '2', 1, '代理'),
       (uuid(), 2, 'order_source_type', '3', 1, '3', 1, '合同'),
       (uuid(), 2, 'order_source_type', '4', 1, '4', 1, '分销商'),
       -- 云订单状态
       (uuid(), 2, 'order_status', '1', 1, '1', 1, '待审核'),
       (uuid(), 2, 'order_status', '2', 1, '2', 1, '待退款'),
       (uuid(), 2, 'order_status', '3', 1, '3', 1, '处理中'),
       (uuid(), 2, 'order_status', '4', 1, '4', 1, '已取消'),
       (uuid(), 2, 'order_status', '5', 1, '5', 1, '已完成'),
       (uuid(), 2, 'order_status', '6', 1, '6', 1, '待支付'),
       (uuid(), 2, 'order_status', '9', 1, '9', 1, '待确认'),
       (uuid(), 2, 'order_status', '10', 1, '10', 1, '待发货'),
       (uuid(), 2, 'order_status', '11', 1, '11', 1, '待收货'),
       (uuid(), 2, 'order_status', '12', 1, '12', 1, '待上门取货'),
       (uuid(), 2, 'order_status', '13', 1, '13', 1, '换新中'),
       -- 订单折扣类型
       (uuid(), 2, 'order_discount_type', '200', 0, '200', 0, '促销产品折扣'),
       (uuid(), 2, 'order_discount_type', '300', 0, '300', 0, '促销折扣券'),
       (uuid(), 2, 'order_discount_type', '301', 0, '301', 0, '促销代金券'),
       (uuid(), 2, 'order_discount_type', '302', 0, '302', 0, '促销现金券'),
       (uuid(), 2, 'order_discount_type', '500', 0, '500', 0, '代理订购指定折扣'),
       (uuid(), 2, 'order_discount_type', '501', 0, '501', 0, '代理订购指定减免'),
       (uuid(), 2, 'order_discount_type', '502', 0, '502', 0, '代理订购指定一口价'),
       (uuid(), 2, 'order_discount_type', '600', 0, '600', 0, '折扣返利合同'),
       (uuid(), 2, 'order_discount_type', '601', 0, '601', 0, '渠道框架合同'),
       (uuid(), 2, 'order_discount_type', '602', 0, '602', 0, '专款专用合同'),
       (uuid(), 2, 'order_discount_type', '603', 0, '603', 0, '线下直签合同'),
       (uuid(), 2, 'order_discount_type', '604', 0, '604', 0, '电销授权合同'),
       (uuid(), 2, 'order_discount_type', '605', 0, '605', 0, '商务合同折扣'),
       (uuid(), 2, 'order_discount_type', '606', 0, '606', 0, '渠道商务合同折扣'),
       (uuid(), 2, 'order_discount_type', '607', 0, '607', 0, '合作伙伴授权折扣'),
       (uuid(), 2, 'order_discount_type', '609', 0, '609', 0, '订单调价折扣'),
       (uuid(), 2, 'order_discount_type', '610', 0, '610', 0, '免单金额'),
       (uuid(), 2, 'order_discount_type', '700', 0, '700', 0, '促销折扣'),
       (uuid(), 2, 'order_discount_type', '800', 0, '800', 0, '充值帐户折扣'),
       -- 账单类型
       (uuid(), 2, 'bill_type', '1', 1, '1', 1, '消费-新购'),
       (uuid(), 2, 'bill_type', '2', 1, '2', 1, '消费-续订'),
       (uuid(), 2, 'bill_type', '3', 1, '3', 1, '消费-变更'),
       (uuid(), 2, 'bill_type', '4', 1, '4', 1, '退款-退订'),
       (uuid(), 2, 'bill_type', '5', 1, '5', 1, '消费-使用'),
       (uuid(), 2, 'bill_type', '8', 1, '8', 1, '消费-自动续订'),
       (uuid(), 2, 'bill_type', '9', 1, '9', 1, '调账-补偿'),
       (uuid(), 2, 'bill_type', '14', 1, '14', 1, '消费-服务支持计划月末扣费'),
       (uuid(), 2, 'bill_type', '16', 1, '16', 1, '调账-扣费'),
       (uuid(), 2, 'bill_type', '18', 1, '18', 1, '消费-按月付费'),
       (uuid(), 2, 'bill_type', '20', 1, '20', 1, '退款-变更'),
       (uuid(), 2, 'bill_type', '23', 1, '23', 1, '消费-节省计划抵扣'),
       (uuid(), 2, 'bill_type', '24', 1, '24', 1, '退款-包年/包月转按需')
;

-- 云镜像类型初始化
truncate table ops_cloud_image_type;
insert into ops_cloud_image_type (it_id, cloud_id, image_type, description, has_os_type)
-- 华为云
values (uuid(), 2, 'gold', '公共镜像', 1),
       (uuid(), 2, 'private', '私有镜像', 0),
       (uuid(), 2, 'shared', '共享镜像', 0),
       (uuid(), 2, 'market', '市场镜像', 0)
;

-- 云镜像系统类型初始化
truncate table ops_cloud_image_os_type;
insert into ops_cloud_image_os_type (ot_id, cloud_id, os_type, platform)
-- 华为云
values (uuid(), 2, 'Windows', 'Windows'),
       (uuid(), 2, 'Linux', 'Debian'),
       (uuid(), 2, 'Linux', 'Ubuntu'),
       (uuid(), 2, 'Linux', 'Red Hat'),
       (uuid(), 2, 'Linux', 'CentOS'),
       (uuid(), 2, 'Linux', 'Fedora'),
       (uuid(), 2, 'Linux', 'SUSE'),
       (uuid(), 2, 'Linux', 'OpenSUSE'),
       (uuid(), 2, 'Linux', 'Oracle Linux'),
       (uuid(), 2, 'Linux', 'CoreOS'),
       (uuid(), 2, 'Linux', 'EulerOS'),
       (uuid(), 2, 'Other', 'Other')
;

-- 云上资源账单信息，分区创建
alter table ops_cloud_resource_bill partition by range columns(bill_cycle_date)
(
        partition p201801 values less than ('2018-02-01'),
        partition p201802 values less than ('2018-03-01'),
        partition p201803 values less than ('2018-04-01'),
        partition p201804 values less than ('2018-05-01'),
        partition p201805 values less than ('2018-06-01'),
        partition p201806 values less than ('2018-07-01'),
        partition p201807 values less than ('2018-08-01'),
        partition p201808 values less than ('2018-09-01'),
        partition p201809 values less than ('2018-10-01'),
        partition p201810 values less than ('2018-11-01'),
        partition p201811 values less than ('2018-12-01'),
        partition p201812 values less than ('2019-01-01'),
        partition p201901 values less than ('2019-02-01'),
        partition p201902 values less than ('2019-03-01'),
        partition p201903 values less than ('2019-04-01'),
        partition p201904 values less than ('2019-05-01'),
        partition p201905 values less than ('2019-06-01'),
        partition p201906 values less than ('2019-07-01'),
        partition p201907 values less than ('2019-08-01'),
        partition p201908 values less than ('2019-09-01'),
        partition p201909 values less than ('2019-10-01'),
        partition p201910 values less than ('2019-11-01'),
        partition p201911 values less than ('2019-12-01'),
        partition p201912 values less than ('2020-01-01'),
        partition p202001 values less than ('2020-02-01'),
        partition p202002 values less than ('2020-03-01'),
        partition p202003 values less than ('2020-04-01'),
        partition p202004 values less than ('2020-05-01'),
        partition p202005 values less than ('2020-06-01'),
        partition p202006 values less than ('2020-07-01'),
        partition p202007 values less than ('2020-08-01'),
        partition p202008 values less than ('2020-09-01'),
        partition p202009 values less than ('2020-10-01'),
        partition p202010 values less than ('2020-11-01'),
        partition p202011 values less than ('2020-12-01'),
        partition p202012 values less than ('2021-01-01'),
        partition p202101 values less than ('2021-02-01'),
        partition p202102 values less than ('2021-03-01'),
        partition p202103 values less than ('2021-04-01'),
        partition p202104 values less than ('2021-05-01'),
        partition p202105 values less than ('2021-06-01'),
        partition p202106 values less than ('2021-07-01'),
        partition p202107 values less than ('2021-08-01'),
        partition p202108 values less than ('2021-09-01'),
        partition p202109 values less than ('2021-10-01'),
        partition p202110 values less than ('2021-11-01'),
        partition p202111 values less than ('2021-12-01'),
        partition p202112 values less than ('2022-01-01'),
        partition p202201 values less than ('2022-02-01'),
        partition p202202 values less than ('2022-03-01'),
        partition p202203 values less than ('2022-04-01'),
        partition p202204 values less than ('2022-05-01'),
        partition p202205 values less than ('2022-06-01'),
        partition p202206 values less than ('2022-07-01'),
        partition p202207 values less than ('2022-08-01'),
        partition p202208 values less than ('2022-09-01'),
        partition p202209 values less than ('2022-10-01'),
        partition p202210 values less than ('2022-11-01'),
        partition p202211 values less than ('2022-12-01'),
        partition p202212 values less than ('2023-01-01'),
        partition p202301 values less than ('2023-02-01'),
        partition p202302 values less than ('2023-03-01'),
        partition p202303 values less than ('2023-04-01'),
        partition p202304 values less than ('2023-05-01'),
        partition p202305 values less than ('2023-06-01'),
        partition p202306 values less than ('2023-07-01'),
        partition p202307 values less than ('2023-08-01'),
        partition p202308 values less than ('2023-09-01'),
        partition p202309 values less than ('2023-10-01'),
        partition p202310 values less than ('2023-11-01'),
        partition p202311 values less than ('2023-12-01'),
        partition p202312 values less than ('2024-01-01'),
        partition p202401 values less than ('2024-02-01'),
        partition p202402 values less than ('2024-03-01'),
        partition pmax values less than maxvalue
);

-- 云上资源账单扩展信息，分区创建
alter table ops_cloud_resource_bill_extra partition by range columns(bill_cycle_date)
(
        partition p201801 values less than ('2018-02-01'),
        partition p201802 values less than ('2018-03-01'),
        partition p201803 values less than ('2018-04-01'),
        partition p201804 values less than ('2018-05-01'),
        partition p201805 values less than ('2018-06-01'),
        partition p201806 values less than ('2018-07-01'),
        partition p201807 values less than ('2018-08-01'),
        partition p201808 values less than ('2018-09-01'),
        partition p201809 values less than ('2018-10-01'),
        partition p201810 values less than ('2018-11-01'),
        partition p201811 values less than ('2018-12-01'),
        partition p201812 values less than ('2019-01-01'),
        partition p201901 values less than ('2019-02-01'),
        partition p201902 values less than ('2019-03-01'),
        partition p201903 values less than ('2019-04-01'),
        partition p201904 values less than ('2019-05-01'),
        partition p201905 values less than ('2019-06-01'),
        partition p201906 values less than ('2019-07-01'),
        partition p201907 values less than ('2019-08-01'),
        partition p201908 values less than ('2019-09-01'),
        partition p201909 values less than ('2019-10-01'),
        partition p201910 values less than ('2019-11-01'),
        partition p201911 values less than ('2019-12-01'),
        partition p201912 values less than ('2020-01-01'),
        partition p202001 values less than ('2020-02-01'),
        partition p202002 values less than ('2020-03-01'),
        partition p202003 values less than ('2020-04-01'),
        partition p202004 values less than ('2020-05-01'),
        partition p202005 values less than ('2020-06-01'),
        partition p202006 values less than ('2020-07-01'),
        partition p202007 values less than ('2020-08-01'),
        partition p202008 values less than ('2020-09-01'),
        partition p202009 values less than ('2020-10-01'),
        partition p202010 values less than ('2020-11-01'),
        partition p202011 values less than ('2020-12-01'),
        partition p202012 values less than ('2021-01-01'),
        partition p202101 values less than ('2021-02-01'),
        partition p202102 values less than ('2021-03-01'),
        partition p202103 values less than ('2021-04-01'),
        partition p202104 values less than ('2021-05-01'),
        partition p202105 values less than ('2021-06-01'),
        partition p202106 values less than ('2021-07-01'),
        partition p202107 values less than ('2021-08-01'),
        partition p202108 values less than ('2021-09-01'),
        partition p202109 values less than ('2021-10-01'),
        partition p202110 values less than ('2021-11-01'),
        partition p202111 values less than ('2021-12-01'),
        partition p202112 values less than ('2022-01-01'),
        partition p202201 values less than ('2022-02-01'),
        partition p202202 values less than ('2022-03-01'),
        partition p202203 values less than ('2022-04-01'),
        partition p202204 values less than ('2022-05-01'),
        partition p202205 values less than ('2022-06-01'),
        partition p202206 values less than ('2022-07-01'),
        partition p202207 values less than ('2022-08-01'),
        partition p202208 values less than ('2022-09-01'),
        partition p202209 values less than ('2022-10-01'),
        partition p202210 values less than ('2022-11-01'),
        partition p202211 values less than ('2022-12-01'),
        partition p202212 values less than ('2023-01-01'),
        partition p202301 values less than ('2023-02-01'),
        partition p202302 values less than ('2023-03-01'),
        partition p202303 values less than ('2023-04-01'),
        partition p202304 values less than ('2023-05-01'),
        partition p202305 values less than ('2023-06-01'),
        partition p202306 values less than ('2023-07-01'),
        partition p202307 values less than ('2023-08-01'),
        partition p202308 values less than ('2023-09-01'),
        partition p202309 values less than ('2023-10-01'),
        partition p202310 values less than ('2023-11-01'),
        partition p202311 values less than ('2023-12-01'),
        partition p202312 values less than ('2024-01-01'),
        partition p202401 values less than ('2024-02-01'),
        partition p202402 values less than ('2024-03-01'),
        partition pmax values less than maxvalue
);

# 以后每个月添加分区
alter table [table_name] reorganize partition [max_partition_name] into
(
        partition [new_partition_name] values less than ([partition]),
        partition [max_partition_name] values less than maxvalue
);
