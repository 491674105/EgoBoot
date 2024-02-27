import gc

# 监听网段及端口
bind = '0.0.0.0:8886'

# worker执行超时，请求处理超过该时长，worker会被重启，默认30s
timeout = 300
# 优雅停机超时，超过该时间还未结束的worker会被强制kill。默认：30s
# graceful_timeout = 30
# HTTP Keep-Alive连接超时，默认2s
keepalive = 5

workers = 1
worker_connections = 1000

# 设置守护进程，可将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'gevent'
# 设置进程文件目录
pidfile = './scheduler_service/scheduler_service.pid'
# 设置访问日志和错误信息日志路径，重定向至标准输出
accesslog = '-'
errorlog = '-'
# 设置日志记录水平
loglevel = 'info'
gc.freeze()
