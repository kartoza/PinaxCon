import os

from settings_prod import *

DEBUG = bool(int(os.environ.get("DEBUG", "1")))

ALLOWED_HOSTS.append("localhost")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECRET_KEY = "6r&z0i#!k-thu4nv^zzx!f$fbp(&#2i5mq_^%%@ihu_qxxotl_"
