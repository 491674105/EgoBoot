#!/bin/bash

. /etc/profile

clean_up() {
	echo "清空编译缓存..."
	find . -type d | grep "__pycache__" | xargs -I {} rm -rf {}
	find . -type f | grep "\.pyc" | xargs -I {} rm -rf {}
	echo "清空编译目标文件、相关配置及本地缓存数据..."
	rm -rf build dist nacos-data
	case $1 in 
		"-a")
			ls | grep -E ".*\.spec" | xargs -I {} rm -rf {}
			;;
		*)
			# ls | grep -E ".*\.spec"
			echo ""
			;;
	esac
}

clean_up $@
