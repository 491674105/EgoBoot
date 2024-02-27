import gc

from env import ENV

# 监听网段及端口
bind = '0.0.0.0:XXXX'

# worker执行超时，请求处理超过该时长，worker会被重启，默认30s
# timeout = 300
# 优雅停机超时，超过该时间还未结束的worker会被强制kill。默认：30s
# graceful_timeout = 30
# HTTP Keep-Alive连接超时，默认2s
# keepalive = 60


# 并行工作进程数 <= (2*CPU_Cores) + 1
#workers = 2
# 每个worker线程数，如有特殊需求再开启
#threads = 2
# 最大并发量 <= worker*1000
#worker_connections = 2000
if ENV in ("prod", "preprod"):
    workers = 4
    # threads = 2
    worker_connections = 4000
elif ENV in ("test", ):
    workers = 2
    # threads = 2
    worker_connections = 2000
else:
    workers = 1
    worker_connections = 1000

# 设置守护进程，可将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'gevent'
# 设置进程文件目录
pidfile = './example_service/example_service.pid'
# 设置访问日志和错误信息日志路径，重定向至标准输出
accesslog = '-'
errorlog = '-'
# 设置日志记录水平
loglevel = 'info'

"""
    1. 调用gc.freeze()必须在fork子进程之前
    2. 在gunicorn初始化配置时调用，freeze把截止到当前的所有对象放入持久化区域，
        不进行回收，从而model占用的内存不会被copy-on-write。
"""
gc.freeze()
