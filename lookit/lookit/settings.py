from pathlib import Path
import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()  # reads .env file

#TEST
# During development, print emails to the console instead of sending them
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nx@ivq@%5^)fwwnv06klo#(7z2%o^%_od@k=1+kk)+vfyf_7q$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

ALLOWED_HOSTS = [
    'lookit.abhinavashokm.site',
    'www.lookit.abhinavashokm.site',
    '3.26.194.155',  # server IP
    'localhost',  # for local development
    '127.0.0.1',  # for local development #for ngrok testing
    'simplistic-pokier-melania.ngrok-free.dev' 
]

#for using tunneling
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.dev']


# Set default user model
AUTH_USER_MODEL = 'user.User'

# GOOGLE RELATED THINGS ------------

# added for continue with google
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Continue with google credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('CLIENT_SECRET')

LOGIN_URL = 'user-login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    # # BLOCK ADMIN BEFORE CREATING SESSION
    # 'user.pipeline.block_admin_google_login',
    # ⚠️ If email exist connect with existing account
    'user.pipeline.link_to_existing_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


SOCIAL_AUTH_ASSOCIATE_BY_EMAIL = True
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
# END GOOGLE RELATED THINGS ---------

# For sending email to user
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my apps
    "user",
    "core",
    "staff",
    "product",
    "cart",
    "order",
    "payment",
    "wallet",
    "coupon",
    "offer",
    
    #extensions
    'social_django',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lookit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ BASE_DIR / "templates" ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                #context processor
                "core.context_processors.cart_item_count"
            ],
        },
    },
]

WSGI_APPLICATION = "lookit.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

#time zone set for timezone.now()
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]


STATIC_ROOT = BASE_DIR / "collected_static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#CLOUDINARY CONFIGURATION {
CLOUDINARY_STORAGE = {
    'CLOUD_NAME':os.getenv('CLOUD_NAME'),
    'API_KEY':os.getenv('API_KEY'),
    'API_SECRET':os.getenv('API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

# Ensure Cloudinary is configured globally for the uploader
cloudinary.config( 
  cloud_name = os.getenv('CLOUD_NAME'),
  api_key = os.getenv('API_KEY'),
  api_secret = os.getenv('API_SECRET'),
  secure = True
)

# }

# ⏰ Session expires after 2 hours (in seconds)
SESSION_COOKIE_AGE = 60 * 60 * 2  # 2 hours

# Razorpay Configurations
RAZOR_KEY_ID = os.getenv('RAZORPAY_API_KEY')
RAZOR_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'


# Security settings for production
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

#bussiness logic configurations
MAX_CART_QUANTITY = 4
COD_MIN_ORDER_AMOUNT = 1000 
OTP_EXPIRY_TIME = 2 #in minutes
RESEND_OTP_AFTER = 1 #in minutes
