# Override settings for G3W-SUITE docker
# Destination: /code/g3w-admin/base/settings/local_settings.py
# Read connection parameters from environment
import os
from django.conf import settings
from base import __version__ as version

# Load custom templates and static files from your docker volume (eg. "./config/g3w-suite/overrides/")
# --------------------------------------------
# https://docs.djangoproject.com/en/2.2/howto/overriding-templates/
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# https://docs.djangoproject.com/en/2.2/topics/settings/
if( version >= (3, 5) ):
    settings.TEMPLATES[0]['DIRS'].append(os.path.join(settings.BASE_DIR, '../../templates')) # /code/templates
    settings.STATICFILES_DIRS.append(os.path.join(settings.BASE_DIR, '../../static'))        # /code/static

G3WADMIN_PROJECT_APPS = []

G3WADMIN_LOCAL_MORE_APPS = [
    'caching',
    'editing',
    'filemanager',
    'qplotly',
    # Uncomment if you wont activate the following module
    #'openrouteservice',
    'qtimeseries',
    'frontend'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('G3WSUITE_POSTGRES_DBNAME'),
        'USER': os.getenv('G3WSUITE_POSTGRES_USER_LOCAL') if os.getenv('G3WSUITE_POSTGRES_USER_LOCAL') else "%s@%s" % (
            os.getenv('G3WSUITE_POSTGRES_USER'), os.getenv('G3WSUITE_POSTGRES_HOST')),
        'PASSWORD': os.getenv('G3WSUITE_POSTGRES_PASS'),
        'HOST': os.getenv('G3WSUITE_POSTGRES_HOST'),
        'PORT': os.getenv('G3WSUITE_POSTGRES_PORT'),
    }
}

MEDIA_ROOT = '/shared-volume/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/shared-volume/static/'
STATIC_URL = '/static/'

DEBUG = True if os.getenv('G3WSUITE_DEBUG', 'False') == 'True' else False

DATASOURCE_PATH = '/shared-volume/project_data/'

# QGIS AUTH DB
# ========================================
# Set the directory where an existing QGIS auth DB can be found or where it will be created if it does not exist (must be writeable from the server).
QGIS_AUTH_DB_DIR_PATH = os.getenv('G3WSUITE_QGIS_AUTH_DB_DIR_PATH', '/shared-volume')
# Full path to a file where the QGIS auth DB master password is saved, if the file does not exists it will be created (directory must be writeable from the server)
# and the QGIS_AUTH_PASSWORD will be saved into the file.
QGIS_AUTH_PASSWORD_FILE = os.getenv('G3WSUITE_QGIS_AUTH_PASSWORD_FILE', '/shared-volume/qgs_dbauth.db')
# Define QGIS auth DB master password that will be placed into the QGIS_AUTH_PASSWORD_FILE if it does not exist.
QGIS_AUTH_PASSWORD = os.getenv('G3WSUITE_QGIS_AUTH_PASSWORD', 'wtsgTgds53fshUHH89UJY')

# CACHING SETTINGS
# =======================================
TILESTACHE_CACHE_NAME = 'default'
TILESTACHE_CACHE_TYPE = 'Disk'  # or 'Memcache'
TILESTACHE_CACHE_DISK_PATH = os.getenv('G3WSUITE_TILECACHE_PATH', '/shared-volume/tile_cache/')
TILESTACHE_CACHE_BUFFER_SIZE = os.getenv('TILESTACHE_CACHE_BUFFER_SIZE', 256)
TILESTACHE_CACHE_TOKEN = os.getenv('TILESTACHE_CACHE_TOKEN', '374h5g96831hsgetvmkdel')

# FILEMANAGER SETTINGS
# =======================================
FILEMANAGER_ROOT_PATH = os.getenv(
    'G3WSUITE_FILEMANAGER_ROOT_PATH', '/shared-volume/project_data')
FILENAMANAGER_MAX_N_FILES = os.getenv('G3WSUITE_FILENAMANAGER_MAX_N_FILES', 10)

# EDITING SETTINGS
# ======================================
USER_MEDIA_ROOT = FILEMANAGER_ROOT_PATH + '/' + \
    os.getenv('G3WSUITE_USER_MEDIA_ROOT', 'user_media') + '/'


# CACHING
# =======================================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# OPENROUTESERVICE SETTINGS
# ===============================
# settings for 'openrouteservice' module is in 'G3WADMIN_LOCAL_MORE_APPS'
# ORS API endpoint
ORS_API_ENDPOINT = os.getenv('ORS_API_ENDPOINT', 'https://api.openrouteservice.org/v2')
# Optional, can be blank if the key is not required by the endpoint
ORS_API_KEY = os.getenv('ORS_API_KEY', '')
# List of available ORS profiles
ORS_PROFILES = {
    "driving-car": {"name": "Car"},
    "driving-hgv": {"name": "Heavy Goods Vehicle"}
}
# Max number of ranges (it depends on the server configuration)
ORS_MAX_RANGES = int(os.getenv('ORS_MAX_RANGES', 6))
# Max number of locations(it depends on the server configuration)
ORS_MAX_LOCATIONS = int(os.getenv('ORS_MAX_LOCATIONS', 2))

# HUEY Task scheduler
# Requires redis
# HUEY configuration
HUEY = {
    # Huey implementation to use.
    'huey_class': 'huey.RedisExpireHuey',
    'name': 'g3w-suite',
    'url': 'redis://redis:6379/?db=0',
    'immediate': False,  # If DEBUG=True, run synchronously.
    'consumer': {
        'workers': 1,
        'worker_type': 'process',
    },
}

# USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = ["*"]

# Is required by caching module
QDJANGO_SERVER_URL = 'http://localhost:8000'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/tmp/error.log',
            'formatter': 'verbose'
        },
        'file_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'g3wadmin.debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'pycsw.server': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'catalog': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'celery.task': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'openrouteservice': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

SESSION_COOKIE_NAME = 'gis3w-suite-v39x-weyiuysajdh'

# Set trust url for http
if os.getenv('WEBGIS_PUBLIC_HOSTNAME', None):
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:8080",
        f"http://{os.getenv('WEBGIS_PUBLIC_HOSTNAME', None)}",
        f"http://{os.getenv('WEBGIS_PUBLIC_HOSTNAME', None)}:8080"
    ]


##################################################################################################################
# customizations: https://g3w-suite.readthedocs.io/en/latest/branding.html
G3WSUITE_CUSTOM_STATIC_URL = '/static/'

G3WSUITE_MAIN_LOGO = '/static/img/logo-home.png'
G3WSUITE_RID_LOGO = '/static/img/logo-home.png'
G3WSUITE_LOGIN_LOGO = '/static/img/logo-home.png'
# G3WSUITE_FAVICON

# G3W-SUITE html page title. If is not set, title is: g3w-admin for admin section and g3w-client for webgis client.
G3WSUITE_CUSTOM_TITLE = 'IGAG WebGIS Lab'

G3WSUITE_CUSTOM_CSS = [
    G3WSUITE_CUSTOM_STATIC_URL + 'css/custom.css'
]

G3WSUITE_POWERD_BY = False

# G3W_CLIENT_HEADER_CUSTOM_LINKS = [
#      {
#          'url': 'https://gis3w.it',
#          'title': 'Gis3W company',
#          'i18n': True, #(False as default value)
#          'target': '_blank',
#          'img': 'https://gis3w.it/wp-content/uploads/2016/10/logo_qgis-1-100x100.png?x22227',
#      },
#      {
#         'title': 'Modal 1',
#         'content': '<p>Html example content to show in modal</p>',
#         'type': 'modal',
#         'position': 10
#     },
# ]

# G3W_CLIENT_LEGEND = {
#    'color': 'red',
#    'fontsize': 8,
#    'transparent': True,
#    'boxspace': 4,
#    'layerspace': 4,
#    'layertitle': True,
#    'layertitlespace': 4,
#    'symbolspace': None,
#    'iconlabelspace': 2,
#    'symbolwidth': 8,
#    'symbolheight': 4
# }

# G3W_CLIENT_RIGHT_PANEL = {
#     'width': 33
# }

FRONTEND = True
FRONTEND_APP = 'frontend'

# -----------------------------------------------------------------------------------------------------
# monkey patch mapLayerAttributesFromQgisLayer() from g3w-admin/core/utils/structure.py 
# https://github.com/g3w-suite/g3w-admin/issues/1074
# -----------------------------------------------------------------------------------------------------
from core.utils import structure
from collections import OrderedDict
from django.urls import reverse

import copy

from qgis.core import QgsFieldConstraints, Qgis, QgsExpression, QgsExpressionNode
from qgis.PyQt.QtCore import QVariant, QDate, QDateTime, NULL

# needed for explode_expression
from qgis.core import QgsExpression
import re

# relations data type
RELATIONS_ONE_TO_ONE = 'ONE'
RELATIONS_ONE_TO_MANY = 'MANY'

# namespace to add 'private' properties to geojson data
RELATIONS_NAMESPACE = 'g3w_'

# data field type for client
# ==========================
FIELD_TYPE_INTEGER = 'integer'
FIELD_TYPE_BIGINTEGER = 'bigint'
FIELD_TYPE_SMALLINTEGER = 'integer'
FIELD_TYPE_FLOAT = 'float'
FIELD_TYPE_STRING = 'string'
FIELD_TYPE_TEXT = 'text'
FIELD_TYPE_BOOLEAN = 'boolean'
FIELD_TYPE_DATE = 'date'
FIELD_TYPE_TIME = 'time'
FIELD_TYPE_DATETIME = 'datetime'
FIELD_TYPE_IMAGE = 'image'
FIELD_TYPE_FILE = 'file'
FIELD_TYPE_VARCHAR = 'varchar'
FIELD_TYPE_CHAR = 'char'

# form field type for editing and forms in general
# ================================================
FORM_FIELD_TYPE_TEXT = 'text'
FORM_FIELD_TYPE_TEXTAREA = 'textarea'
FORM_FIELD_TYPE_SELECT = 'select'
FORM_FIELD_TYPE_SELECT_AUTOCOMPLETE = 'select_autocomplete'
FORM_FIELD_TYPE_CHECK = 'check'
FORM_FIELD_TYPE_RADIO = 'radio'
FORM_FIELD_TYPE_COORDSPICKER = 'coordspicker'
FORM_FIELD_TYPE_BOXPICKER = 'boxspicker'
FORM_FIELD_TYPE_LAYERPICKER = 'layerpicker'
FORM_FIELD_TYPE_FIELDDEPEND = 'fielddepend'
FORM_FIELD_TYPE_IMAGE = 'image'
FORM_FIELD_TYPE_FILE = 'file'
FORM_FIELD_TYPE_FLOAT = 'float'


# mapping between form fields and fields data types
# =================================================
FORM_FIELDS_MAPPING = {
    FIELD_TYPE_INTEGER: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_BIGINTEGER: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_FLOAT: FORM_FIELD_TYPE_FLOAT,
    FIELD_TYPE_STRING: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_TEXT: FORM_FIELD_TYPE_TEXTAREA,
    FIELD_TYPE_VARCHAR: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_CHAR: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_BOOLEAN: FORM_FIELD_TYPE_RADIO,
    FIELD_TYPE_DATE: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_TIME: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_DATETIME: FORM_FIELD_TYPE_TEXT,
    FIELD_TYPE_IMAGE: FORM_FIELD_TYPE_IMAGE,
    FIELD_TYPE_FILE: FORM_FIELD_TYPE_FILE,
}




FIELD_TYPES_MAPPING = {
    'BOOL': FIELD_TYPE_BOOLEAN,
    'INT': FIELD_TYPE_INTEGER,
    'UINT': FIELD_TYPE_INTEGER,
    'QLONGLONG': FIELD_TYPE_BIGINTEGER,
    'QULONGLONG': FIELD_TYPE_BIGINTEGER,
    'DOUBLE': FIELD_TYPE_FLOAT,
    'QCHAR': FIELD_TYPE_CHAR,
    'QSTRING': FIELD_TYPE_VARCHAR,
    'QDATE': FIELD_TYPE_DATE,
    'QTIME': FIELD_TYPE_TIME,
    'QDATETIME': FIELD_TYPE_DATETIME,
    'QURL': FIELD_TYPE_VARCHAR,
    'LONG': FIELD_TYPE_FLOAT,
    'SHORT': FIELD_TYPE_FLOAT,
    'CHAR': FIELD_TYPE_CHAR,
    'ULONG': FIELD_TYPE_FLOAT,
    'USHORT': FIELD_TYPE_FLOAT,
    'UCHAR': FIELD_TYPE_CHAR,
    'FLOAT': FIELD_TYPE_FLOAT,
    'PYQT_PYOBJECT': FIELD_TYPE_VARCHAR, # For not main geometry field
}


# this is from qdjango/utils/qgis.py
def explode_expression(expression):
    """
    Give a string expression return metadata information like column names and qgis expression functions
    :param expression: String QGIS expression
    :return type: dict
    :return: Dict of QGIS expression metadata info.
    """

    exp = QgsExpression(expression)
    filter_expression = {
        'expression': exp.expression(),
        'referenced_columns': list(exp.referencedColumns()),
        'referenced_functions': list(exp.referencedFunctions())
    }

    # For current_values function in filter expression get parameter field fo it
    if "current_value" in filter_expression['referenced_functions']:
        groups = re.findall(r'current_value[^\S]*\([^\S]?[\'"|\\\'](.*?)["\'|\\\'][^\S]?\)|(\w+=\w+)',
                            filter_expression['expression'])
        filter_expression['referencing_fields'] = [g[0] for g in groups]

    return filter_expression


def editingFormField(fieldName, type=FIELD_TYPE_STRING, editable=True, required=False, validate=None,
                     fieldLabel=None, inputType=None, values=None, default_clause='', unique=False, expression='',
                     pk=False, ** kwargs):
    """
    Build editing form field for client.
    """

    validate = {}
    if required:
        validate['required'] = True
    if unique:
        validate['unique'] = True
    if expression:
        validate['expression'] = expression

    ret = OrderedDict({
        'name': fieldName,
        'type': type,
        'label': fieldLabel if fieldLabel else fieldName,
        'editable': editable,
        'validate': validate,
        'pk': pk,
        'default': default_clause,
        'input': {
            'type': inputType if inputType else FORM_FIELD_TYPE_TEXT,
            'options': {}
        },
    })

    if required:
        ret['validate']['required'] = True

    if 'default' in kwargs and kwargs['default'] is not None:
        ret['input']['options']['default'] = kwargs['default']

    if inputType in (FORM_FIELD_TYPE_LAYERPICKER, ) and 'pickerdata' in kwargs:
        ret['input']['options'] = kwargs['pickerdata']

    if values:
        ret['input']['options']['values'] = values

    return ret

# Copyright Ferry Boender, released under the MIT license.
def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in list(src.items()):
        if type(v) == list:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if not k in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)

def mapLayerAttributesFromQgisLayer(qgis_layer, **kwargs):
    """
    map QGIS layer's simple and direct field to Attributes for client editing system
    only concrete field not virtual field and many2many
    """

    # Set fields to exclude
    fieldsToExclude = kwargs['exclude'] if 'exclude' in kwargs else []

    toRes = OrderedDict()
    fields = qgis_layer.fields()

    data_provider = qgis_layer.dataProvider()

    field_index = 0

    pk_attributes = qgis_layer.primaryKeyAttributes()

    # Get available Join's fields
    join_fields = {}
    for order, join in enumerate(qgis_layer.vectorJoins()):
        join_id = f'{qgis_layer.id()}_vectorjoin_{order}'
        joinlayer_pk_attributes = join.joinLayer().primaryKeyAttributes()
        for i, f in enumerate(join.joinLayer().fields()):
            editable = join.isEditable()

            # Check if referencing field is PK
            if i in joinlayer_pk_attributes:
                editable = False
            join_fields[join.prefixedFieldName(f)] = {
                'editable': editable,
                'join_id': join_id}


    # Determine if we are using an old and bugged version of QGIS
    IS_QGIS_3_10 = Qgis.QGIS_VERSION.startswith('3.10')

    # FIXME: find better way for layer join 1:1 managment
    for field in fields:
        if field.name() not in fieldsToExclude and field.name() in kwargs['fields']:

            editor_widget_setup = field.editorWidgetSetup()
            internal_typename = QVariant.typeToName(field.type()).upper()
            if internal_typename in FIELD_TYPES_MAPPING:

                # Get constraints and default clause to define if the field is editable
                # or set editable property by kwargs.
                # Only consider "strong" constraints
                constraints = qgis_layer.fieldConstraints(field_index)
                not_null = bool(constraints & QgsFieldConstraints.ConstraintNotNull) and \
                    field.constraints().constraintStrength(
                        QgsFieldConstraints.ConstraintNotNull) == QgsFieldConstraints.ConstraintStrengthHard
                unique = bool(constraints & QgsFieldConstraints.ConstraintUnique) and \
                    field.constraints().constraintStrength(
                        QgsFieldConstraints.ConstraintUnique) == QgsFieldConstraints.ConstraintStrengthHard
                has_expression = bool(constraints & QgsFieldConstraints.ConstraintExpression) and \
                    field.constraints().constraintStrength(
                        QgsFieldConstraints.ConstraintExpression) == QgsFieldConstraints.ConstraintStrengthHard
                default_clause = data_provider.defaultValueClause(field_index)
                default_clause = default_clause if default_clause != 'nextval(NULL)' else ''

                # default value for editing from qgis_layer
                if 'default' not in kwargs:
                    default_value = qgis_layer.defaultValue(field_index) if qgis_layer.defaultValue(field_index) not in (None, NULL) \
                        else None
                else:
                    default_value = kwargs['default']

                if isinstance(default_value, QDate) or isinstance(default_value, QDateTime):
                    try:
                        default_value = default_value.toString(
                            kwargs['fields'][field.name()]['input']['options']['formats'][0]['displayformat'])
                    except Exception as e:
                        default_value = ''

                expression = ''
                if has_expression:
                    expression = field.constraints().constraintExpression()

                if not_null and unique and default_clause:
                    editable = False
                else:
                    try:
                        editable = kwargs['fields'][field.name()]['editable']
                    except Exception as e:
                        editable = False

                # remove editable from kwargs:
                try:
                    del(kwargs['fields'][field.name()]['editable'])
                except Exception as e:
                    pass

                comment = field.comment() if field.comment() else field.name()
                fieldType = FIELD_TYPES_MAPPING[internal_typename]

                if IS_QGIS_3_10:
                    is_pk = unique and default_clause and not_null
                else:
                    is_pk = (field_index in pk_attributes)

                toRes[field.name()] = editingFormField(
                    field.name(),
                    required=not_null,
                    fieldLabel=comment,
                    type=fieldType,
                    inputType=FORM_FIELDS_MAPPING[fieldType],
                    editable=editable,
                    default_clause=default_clause,
                    unique=unique,
                    expression=expression,
                    pk=is_pk,
                    default=default_value
                )

                # add upload url to image type if module is set
                if 'editing' in settings.G3WADMIN_LOCAL_MORE_APPS:
                    if fieldType == FIELD_TYPE_IMAGE:
                        toRes[field.name()].update({
                            'uploadurl': reverse('editing-upload')
                        })

                # update with fields configs data
                if 'fields' in kwargs and field.name() in kwargs['fields']:
                    deepupdate(toRes[field.name()],
                               kwargs['fields'][field.name()])

                    # For default value priority to `default_value`
                    if default_value:
                        toRes[field.name()]['input']['options']['default'] = default_value

                    if fieldType == FIELD_TYPE_BOOLEAN:
                        toRes[field.name()]['input']['options']['values'] = [
                                {'checked': True, 'value': True},
                                {'checked': False, 'value': False}
                            ]

                    # Add multiline and html capabilities for TextEdit widget
                    if editor_widget_setup.type() == 'TextEdit':
                        config = editor_widget_setup.config()
                        if 'IsMultiline' in config and config['IsMultiline'] is True:
                            toRes[field.name()]['input']['type'] = 'textarea'
                        if 'UseHtml' in config and config['UseHtml'] is True:
                            toRes[field.name()]['input']['type'] = 'texthtml'

                # Check for defaultValueDefinition with expression
                # 2021/10/04 snippet by Alessandro Pasotti (elpaso)
                has_default_value_expression = False
                if field.defaultValueDefinition().expression() != '':
                    exp = QgsExpression(field.defaultValueDefinition().expression())
                    if exp.rootNode().nodeType() != QgsExpressionNode.ntLiteral:
                        toRes[field.name()]['input']['options']['default_expression'] = \
                            explode_expression(field.defaultValueDefinition().expression())

                        # Check update if expression default value has to run also on update e not
                        # only on insert newone
                        toRes[field.name()]['input']['options']['default_expression']['apply_on_update'] = True \
                            if field.defaultValueDefinition().applyOnUpdate() else False

                # Check for Join's field.
                # About joins in QGIS control the join settings for editing.
                try:
                    toRes[field.name()]['vectorjoin_id'] = join_fields[field.name()]['join_id']
                    toRes[field.name()]["editable"] = join_fields[field.name()]["editable"]
                except:
                    pass

        field_index += 1

    return toRes

# apply monkey patch
structure.mapLayerAttributesFromQgisLayer = mapLayerAttributesFromQgisLayer