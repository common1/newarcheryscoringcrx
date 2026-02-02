from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "_5cccv_d*k!gvkthvdsl)$f-^*gxe!5-&)zhp^=(j#4%fxio3f"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [  # noqa
    "django_sass",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass

# CRX_BANNER = "Development"
# CRX_BANNER_BACKGROUND = '#FFFFE0'   # light yellow background
# CRX_BANNER_TEXT_COLOR = '#000'              # black text color