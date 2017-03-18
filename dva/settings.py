"""
Django settings for dva project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os,dj_database_url,sys
from dvalib import external_indexed

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'changemeabblasdasbdbrp2$j&^' # change this in prod

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"] # Dont use this in prod

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

Q_EXTRACTOR = 'qextract'
Q_INDEXER = 'qindexer'
Q_DETECTOR = 'qdetector'
Q_RETRIEVER = 'qretriever'
Q_FACE_RETRIEVER = 'qfaceretriever'
Q_FACE_DETECTOR = 'qfacedetector'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dvaapp',
    'djcelery'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dva.urls'
PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates/'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dva.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
if sys.platform == 'darwin':
    BROKER_URL = 'amqp://{}:{}@localhost//'.format('dvauser','localpass')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dvadb',
            'USER': 'dvauser',
            'PASSWORD': 'localpass',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
elif 'CONTINUOUS_INTEGRATION' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    BROKER_URL = 'amqp://{}:{}@localhost//'.format('guest','guest')
elif 'DOCKER_MODE' in os.environ:
    BROKER_URL = 'amqp://{}:{}@{}//'.format(os.environ.get('RABBIT_USER','dvauser'),os.environ.get('RABBIT_PASS','localpass'),os.environ.get('RABBIT_HOST','rabbit'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME','postgres'),
            'USER': os.environ.get('DB_USER','postgres'),
            'PASSWORD': os.environ.get('DB_PASS','postgres'),
            'HOST': os.environ.get('DB_HOST','db'),
            'PORT': 5432,
        }
    }



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = '/Users/aub3/media/' if sys.platform == 'darwin' else os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)


STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TASK_NAMES_TO_QUEUE = {
    "inpcetion_index_by_id":Q_INDEXER,
    "inception_query_by_image":Q_RETRIEVER,
    "facenet_query_by_image":Q_FACE_RETRIEVER,
    "extract_frames_by_id":Q_EXTRACTOR,
    "perform_ssd_detection_by_id":Q_DETECTOR,
    "perform_face_detection_indexing_by_id":Q_FACE_DETECTOR
}

POST_OPERATION_TASKS = {
    "extract_frames_by_id":['perform_ssd_detection_by_id',
                            'inpcetion_index_by_id',
                            'perform_face_detection_indexing_by_id']
    }

VISUAL_INDEXES = {
    'inception':
        {
            'indexer_task':"inpcetion_index_by_id",
            'indexer_queue':Q_INDEXER,
            'retriever_queue':Q_RETRIEVER,
            'detection_specific':False
        },
    'facenet':
        {
            'indexer_task': "perform_face_detection_indexing_by_id",
            'indexer_queue': Q_FACE_DETECTOR,
            'retriever_queue': Q_FACE_RETRIEVER,
            'detection_specific': True
        },
    }

EXTERNAL_DATASETS = {
    'products':external_indexed.ProductsIndex(path="{}/external/{}".format(MEDIA_ROOT,'products')),
    'visual_genome':external_indexed.VisualGenomeIndex(path="{}/external/{}".format(MEDIA_ROOT,'products')),
}

for create_dirname in ['queries','external']:
    if not os.path.isdir("{}/{}".format(MEDIA_ROOT,create_dirname)):
        try:
            os.mkdir("{}/{}".format(MEDIA_ROOT,create_dirname))
        except:
            pass

if 'ALEX_ENABLE' in os.environ:
    TASK_NAMES_TO_QUEUE['alexnet_index_by_id'] = Q_INDEXER
    TASK_NAMES_TO_QUEUE['alexnet_query_by_image'] = Q_RETRIEVER
    POST_OPERATION_TASKS['extract_frames_by_id'].append('alexnet_index_by_id')
    VISUAL_INDEXES['alexnet'] = {
         'indexer_task': "alexnet_index_by_id",
         'indexer_queue': Q_INDEXER,
         'retriever_queue': Q_RETRIEVER,
         'detection_specific': False
    }


if 'YOLO_ENABLE' in os.environ:
    TASK_NAMES_TO_QUEUE['perform_yolo_detection_by_id'] = Q_DETECTOR
    POST_OPERATION_TASKS['extract_frames_by_id'].append('perform_yolo_detection_by_id')