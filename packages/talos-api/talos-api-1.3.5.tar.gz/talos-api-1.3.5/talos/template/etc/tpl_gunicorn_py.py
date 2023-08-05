# coding=utf-8

TEMPLATE = u'''${sys_default_coding}

from __future__ import absolute_import

import os
import logging
from logging.handlers import WatchedFileHandler
import multiprocessing

from talos.core import config as __config

__config.setup(os.environ.get('${pkg_name.upper()}_CONF', '${config_file}'),
               dir_path=os.environ.get('${pkg_name.upper()}_CONF_DIR', '${config_dir}'))
CONF = __config.CONF

name = CONF.locale_app
proc_name = CONF.locale_app
bind = '%s:%d' % (CONF.server.bind, CONF.server.port)
backlog = CONF.server.backlog
# 超时
timeout = 30
# 进程数
workers = multiprocessing.cpu_count() * 2
# 指定每个进程开启的线程数
threads = 1
debug = False
daemon = False
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = CONF.log.level.lower()
# 访问日志文件的路径
accesslog = "/dev/null"
# 错误日志文件的路径
errorlog = "/dev/null"
acclog = logging.getLogger('gunicorn.access')
acclog.addHandler(WatchedFileHandler(CONF.log.gunicorn_access))
acclog.propagate = False
errlog = logging.getLogger('gunicorn.error')
errlog.addHandler(WatchedFileHandler(CONF.log.gunicorn_error))
errlog.propagate = False

# keyfile =
# certfile =
# ca_certs =
# chdir = '/home/user'
# sync/gevent/eventlet/tornado/gthread/gaiohttp
# worker_class = 'gevent'
# worker_connections = 1000
# 到达max requests之后worker会重启
# max_requests = 0
# keepalive = 5
# reload = True
# %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
# access_log_format = CONF.log.format_string
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(L)s %(b)s "%(f)s" "%(a)s"'
# syslog_addr = udp://localhost:514
# HTTP URL长度限制
# limit_request_line = 4094
'''