# 运维平台 

## python-yw-ops

## 创建虚拟环境

**_建议使用，避免与系统默认的 python-lib 发生冲突，同时，尽可能保证当前项目的 lib 为清洁环境。_**

```shell
# 创建虚拟环境，并注入相关依赖
python3 -m venv [venv_path]

# 激活虚拟环境
source [venv_path]/bin/activate

# 退出虚拟环境
deactivate
```

## QuickStart

```shell
Python3
pip install -r requirements.txt
```

## 查询服务列表

```shell
# 查询结果包含对应服务启动方式
# 使用服务名关键字查询
python3 starter.py -q [[service_name]-keyword]

# 查询所有服务
python3 starter.py -a
```

## 启动

```shell
python3 starter.py -s [service_name]
```

## 项目目录结构

```
.
|---- core                       核心包
|---- |---- flask_core           Flask核心封装
|---- |---- common
|---- |---- |---- constant       常量
|---- |---- |---- enum           枚举
|---- |---- bootstrap
|---- |---- |---- Config.py      核心配置包
|---- |---- classloader          类加载器包
|---- |---- dispatch             调度器包
|---- |---- exception            异常封装包
|---- |---- request              请求实体封装
|---- |---- entity               实体封装
|---- |---- dao                  公用数据处理层(DAO)
|---- |---- response             响应实体封装
|---- |---- filter               过滤器核心包
|---- |---- interceptor          拦截器核心包
|---- |---- logger               日志处理封装包
|---- |---- network              网络模块
|---- |---- utils                工具类
|---- |---- resources            公用资源
|---- |---- nacos_core           nacos-sdk封装

|---- [service_name]_service     服务包
|---- |---- dispatch             服务调度器
|---- |---- filter               服务自定义过滤器
|---- |---- interceptor          服务自定义拦截器
|---- |---- request              服务请求对象封装
|---- |---- feign                微服务客户端
|---- |---- controller           服务API层
|---- |---- service              服务Service层
|---- |---- task                 调度计划任务
|---- |---- dao                  服务DAO层
|---- |---- resources            服务资源
|---- |---- logs                 服务日志路径

|---- .gitattributes             git 属性配置
|---- .gitignore                 git 忽略配置
|---- clean.sh                   项目缓存清空（服务端建议每次运行缓存清理后启动）
|---- env.py                     环境变量
|---- requirements.txt           依赖
|---- shutdown.sh                一键停服脚本
|---- start_up.sh                一键启动脚本
└---- starter.py                 项目启动入口
```

## Flask-SQLAlchemy

### sqlalchemy 常用数据类型

|  类型名  |    类型归属    | 备注                                                                                                                                     |
| :----: | :----: | :---- |
| BigInteger  |     长整形      | 映射到数据库中是 int 类型                                                                                                                |
| Integer  |      整形      | 映射到数据库中是 int 类型                                                                                                                |
|  Float   |    浮点类型    | 映射到数据库中是 float 类型 32 位                                                                                                        |
|  Double  | 双精度浮点类型 | 映射到数据库中是 double 类型 64 位                                                                                                       |
|  String  |  可变字符类型  | 映射到数据库中是 varchar 类型                                                                                                            |
| Boolean  |    布尔类型    | 映射到数据库中的是 tinyint 类型                                                                                                          |
| DECIMAL  |    定点类型    | 用于解决浮点类型精度丢失的问题。使用时需要传递两个参数，第一个参数是用来标记这个字段总能能存储多少个数字，第二个参数表示小数点后有多少位 |
|   Enum   |    枚举类型    | 指定某个字段只能是枚举中指定的几个值，不能为其他值。在 ORM 模型中，使用 Enum 来作为枚举                                                  |
|   Date   |    日期类型    | 存储时间，只能存储年月日。映射到数据库中是 date 类型。在 Python 代码中，可以使用 datetime.date 来指定                                    |
| DateTime |  日期时间类型  | 存储时间，可以存储年月日时分秒毫秒等。映射到数据库中也是 datetime 类型。在 Python 代码中，可以使用 datetime.datetime 来指定              |
|   Time   |    时间类型    | 存储时间，可以存储时分秒。映射到数据库中也是 time 类型。在 Python 代码中，可以使用 datetime.time 来指定                                  |
|   Text   |     字符串     | 存储长字符串。一般可以存储 6W 多个字符。如果超出了这个范围，可以使用 LONGTEXT 类型。映射到数据库中就是 text 类型                         |
| LONGTEXT |   长文本类型   | 映射到数据库中是 longtext 类型                                                                                                           |

### 字段常用的属性设置

- primary_key：设置某个字段为主键。
- autoincrement：设置这个字段为自动增长的。
- default：设置某个字段的默认值。在发表时间这些字段上面经常用。
- nullable：指定某个字段是否为空。默认值是 True，就是可以为空。
- unique：指定某个字段的值是否唯一。默认是 False。
- onupdate：在数据更新的时候会调用这个参数指定的值或者函数。在第一次插入这条数据的时候，不会用 onupdate 的值，只会使用 default 的值。常用的就是 update_time（每次更新数据的时候都要更新的值）。
- name：指定 ORM 模型中某个属性映射到表中的字段名。如果不指定，那么会使用这个属性的名字来作为字段名。如果指定了，就会使用指定的这个值作为参数。这个参数也可以当作位置参数，在第 1 个参数来指定。
- comment：设置该字段的注释

## 项目安装问题处理

- 安装 MySQL-python ，结果出错 ImportError: No module named 'ConfigParser'

```
在 Python 3.x 版本后，ConfigParser.py 已经更名为 configparser.py 所以出错！
解决方法：pip install mysqlclient
```

- 安装依赖过程中，如果出现“OSError: mysql_config not found”

```
# ubuntu
sudo apt-fast install libmysqlclient-dev python3-dev

# centos
yum -y install libmysqlclient-dev python3-dev
```

- 启动过程中，如果出现“ModuleNotFoundError: No module named flask.\_compat”，这是由于新版 Flask_script 的依赖路径发生了变化

```
# 可以将flask版本进行回退
pip uninstall Flask
pip install Flask==1.1.2

# 或者手动调整相关依赖
vim [python3_lib_path]/.../flask_script/__init__.py
## 注释该行
from flask._compat import text_type
## 重新引入
from flask_script._compat import text_type
```

## 打包

避免生产环境单独部署依赖导致与原来的环境冲突

### 安装工具

```shell
pip install pyinstaller
```

| 命令 | 简写 | 描述 |
| :----: | :----: | :----: |
| --help | -h | 查看该模块的帮助信息 |
| -onefile | -F | 产生单个的可执行文件 |
| --onedir | -D | 产生一个目录（包含多个文件）作为可执行程序 |
| --ascii | -a | 不包含 Unicode 字符集支持 |
| --debug | -d | 产生 debug 版本的可执行文件 |
| --windowed，--noconsolc | -w | 指定程序运行时不显示命令行窗口（仅对 Windows 有效） |
| --nowindowed，--console | -c | 指定使用命令行窗口运行程序（仅对 Windows 有效） |
| --out=DIR | -o DIR | 指定 spec 文件的生成目录。如果没有指定，则默认使用当前目录来生成 spec 文件 |
| --path=DIR | -p DIR | 设置 Python 导入模块的路径（和设置 PYTHONPATH 环境变量的作用相似）。也可使用路径分隔符（Windows 使用分号，Linux 使用冒号）来分隔多个路径 |
| --name=NAME | -n NAME | 指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字 |

### 单脚本打包

```shell
pyinstaller -F [src_file]
```

### 项目打包

```shell
# 生成默认编译配置
pyi-makespec -w [src_file]

# 编译打包
pyinstaller -D [spec_file]
```

#### spec 文件中主要包含 4 个 class: Analysis, PYZ, EXE 和 COLLECT

- Analysis：以 py 文件为输入，它会分析 py 文件的依赖模块，并生成相应的信息
- PYZ：是一个.pyz 的压缩包，包含程序运行需要的所有依赖
- EXE：根据上面两项生成
- COLLECT：生成其他部分的输出文件夹，COLLECT 也可以没有

1. py 文件打包配置  
   针对多目录多文件的 python 项目，打包时候需要将所有相关的 py 文件输入到 Analysis 类里。Analysis 类中的 pathex 定义了打包的主目录，对于在此目录下的 py 文件可以只写文件名不写路径。如上的 spec 脚本，将所有项目中的 py 文件路径以列表形式写入 Analysis，这里为了说明混合使用了绝对路径和相对路径。

2. 资源文件打包配置  
   资源文件包括打包的 python 项目使用的相关文件，如图标文件，文本文件等。对于此类资源文件的打包需要设置 Analysis 的 datas，如例子所示 datas 接收元组：datas=[(SETUP_DIR+'img','img')]。元组的组成为(原项目中资源文件路径，打包后路径)，例子中的(SETUP_DIR+'img','img')表示从 D:\Python\untitled1\下的 img 文件夹文件打包后放入打包结果路径下的 img 目录。

3. Hidden import 配置  
   pyinstaller 在进行打包时，会解析打包的 python 文件，自动寻找 py 源文件的依赖模块。但是 pyinstaller 解析模块时可能会遗漏某些模块（not visible to the analysis phase），造成打包后执行程序时出现类似 No Module named xxx。这时我们就需要在 Analysis 下 hiddenimports 中加入遗漏的模块

4. 递归深度设置  
   在打包导入某些模块时，常会出现"RecursionError: maximum recursion depth exceeded"的错误，这可能是打包时出现了大量的递归超出了 python 预设的递归深度。因此需要在 spec 文件上添加递归深度的设置，设置一个足够大的值来保证打包的进行，即

```python
import sys
sys.setrecursionlimit(5000)
```

## 日志清理
```shell
echo "00 01 01 * * /bin/env bash /usr/local/src/py_yw_ops_log_del.sh" >> /etc/crontab
```
### 脚本内容
___按需调整即可___
```shell
#!/bin/bash

. /etc/profile

LOG_PATH="/opt/app/python-yw-ops/"

delete_log (){
    # 删除7天前的日志
    su - operations -c "find ${LOG_PATH} -mtime +7 -type f | grep \"_service/logs/\" | grep -E \"\.(log|txt).*\" | xargs -I {} rm -rf {}"
}

delete_log
```