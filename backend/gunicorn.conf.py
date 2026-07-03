import os
import multiprocessing

# Gunicorn configuration for production deployment
bind = "0.0.0.0:" + os.getenv("PORT", "5050")
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
timeout = int(os.getenv("TIMEOUT", "120"))
keepalive = 5
loglevel = os.getenv("LOG_LEVEL", "info")
accesslog = "-"
errorlog = "-"
