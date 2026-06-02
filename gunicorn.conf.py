"""
==========================================================================
 GUNICORN PRODUCTION CONFIG - SERPTECH-Software+Accounting-Isolated-Database-35
==========================================================================
 Panduan deploy:
   gunicorn -c gunicorn.conf.py config.wsgi:application
==========================================================================
"""
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
proc_name = "serptech_acc_db"
limit_request_line = 4096
limit_request_fields = 100
forwarded_allow_ips = "*"
graceful_timeout = 30
