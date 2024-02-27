
-- 端口字典
drop table if exists ports;
create table if not exists ports(
	port int not null comment '端口值',
	type tinyint(2) not null comment '端口类型',
	status tinyint(1) not null default 0 comment '端口状态（0：空闲 1：占用）',
	reuse tinyint(1) not null default 0 comment '是否复用（0：否 1：是）',
	primary key(port)
) ENGINE=InnoDB AUTO_INCREMENT=443 DEFAULT CHARSET=utf8;
truncate table ports;

drop procedure if exists create_port_dict;

delimiter //
create procedure create_port_dict()
begin
	set @port = 443;
	set @type = 0;
	set @count = 0;
	set @max_count = 65535 - @port + 1;
	while @count < @max_count do	
		if @port <= 35000 then
			set @type = 0;
		elseif @port > 35000 and @port < 36000 then
			set @type = 1;
		else
			set @type = 2;
		end if;
	
		set @insert_sql = concat('insert into ports(port, type, status) values(', @port, ', ', @type, ', ', 0, ')', ';');
		prepare stmt from @insert_sql;
		execute stmt;
	
		set @port = @port + 1;
		set @count = @count + 1;
	end while;
end //;

call create_port_dict();

-- 更新端口使用状态
update ports p, service s 
set p.status = 1
where p.port = s.port;
