import os
import pathlib
from copy import deepcopy

from .secrets import MONGO_PASSWORD
from .utils import read_endpoint_files

DOMAIN_DIR = pathlib.Path(__file__).parent / "domain"

DOMAIN = read_endpoint_files(DOMAIN_DIR)

URL_PREFIX = os.getenv("XESTORE_URL_PREFIX", "")
API_VERSION = "v1"
RESOURCE_METHODS = ["GET", "POST"]
ITEM_METHODS = ["GET", "PUT", "PATCH", "DELETE"]
ALLOWED_READ_ROLES = ["admin", "superuser", "expert", "user", "read", "write"]
ALLOWED_WRITE_ROLES = ["admin", "superuser", "expert", "write"]
EMBEDDING = True

PAGINATION_LIMIT = 10000
SCHEMA_ENDPOINT = "schema"
IF_MATCH = True
ENFORCE_IF_MATCH = False
HATEOAS = True
VERSIONS = "_versions"
VERSION_ID_SUFFIX = "_document"
NORMALIZE_ON_PATCH = False
RETURN_MEDIA_AS_URL = True
RETURN_MEDIA_AS_BASE64_STRING = False
MEDIA_PATH = "media"
EXTENDED_MEDIA_INFO = ['content_type', 'length']
MULTIPART_FORM_FIELDS_AS_JSON = True

# ----------------- Mongo config ------------------------------------------ #
MONGO_HOST = os.getenv("XESTORE_MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("XESTORE_MONGO_PORT", 27017))
MONGO_DBNAME = os.getenv("XESTORE_MONGO_DB", "pmts")
MONGO_USERNAME = os.getenv("XESTORE_MONGO_USER", "")
MONGO_AUTH_SOURCE = os.getenv("XESTORE_MONGO_AUTH_SOURCE", MONGO_DBNAME)

MONGO1T_HOST = MONGO_HOST
MONGO1T_PORT = MONGO_PORT
MONGO1T_DBNAME = MONGO_DBNAME + "1t"
MONGO1T_AUTH_SOURCE = MONGO_AUTH_SOURCE
MONGO1T_PASSWORD = MONGO_PASSWORD
if os.getenv("XESTORE_MONGO_REPLICA_SET", ""):
    MONGO_REPLICA_SET = os.getenv("XESTORE_MONGO_REPLICA_SET", "")
    MONGO1T_REPLICA_SET = MONGO_REPLICA_SET

MONGO1T_USERNAME = MONGO_USERNAME

if os.getenv("XESTORE_MONGO_URI", ""):
    MONGO_URI = os.getenv("XESTORE_MONGO_URI", "")
    MONGO1T_URI = MONGO_URI
# -------------------------------------------------------------------------- #

SERVERS = [
    "https://xestore-dot-xenon-pmts.uc.r.appspot.com",
    "https://api."+os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org'),
    "http://localhost:5000",
    ]

X_DOMAINS = ['http://localhost:8000',
            'http://127.0.0.1:8000',
            'http://127.0.0.1:5000',
            'http://editor.swagger.io',
            "https://"+os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org'),
            "https://api."+os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org'),
            "https://website."+os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org'),
            "https://panels."+os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org'),
            "https://catalog."+os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org'),
             ]

X_HEADERS = ['Content-Type', 'If-Match', 'Authorization', 'X-HTTP-Method-Override']  # Needed for the "Try it out" buttons

JWT_AUDIENCES = []#["xestore_client"]
JWT_KEY_URL = f"https://{os.getenv('XESTORE_DOMAIN','pmts.xenonnt.org')}/db_api/certs/"
JWT_SCOPE_CLAIM = None
JWT_ROLES_CLAIM = "roles"
JWT_TTL = 3600

def get_settings_dict(**overrides):
    domain_overrides = overrides.pop("DOMAIN", {})
    domain = dict(DOMAIN)
    domain.update(domain_overrides)

    settings = dict(
        DOMAIN = domain,
        URL_PREFIX = URL_PREFIX,
        API_VERSION = API_VERSION,
        RESOURCE_METHODS = RESOURCE_METHODS,
        ITEM_METHODS = ITEM_METHODS,
        ALLOWED_READ_ROLES = ALLOWED_READ_ROLES,
        ALLOWED_WRITE_ROLES = ALLOWED_WRITE_ROLES,
        EMBEDDING = EMBEDDING,
        MEDIA_PATH = MEDIA_PATH,
        PAGINATION_LIMIT = PAGINATION_LIMIT,
        SCHEMA_ENDPOINT = SCHEMA_ENDPOINT,
        IF_MATCH = IF_MATCH,
        ENFORCE_IF_MATCH = ENFORCE_IF_MATCH,
        HATEOAS = HATEOAS,
        VERSIONS = VERSIONS,
        VERSION_ID_SUFFIX = VERSION_ID_SUFFIX,
        NORMALIZE_ON_PATCH = NORMALIZE_ON_PATCH,
        RETURN_MEDIA_AS_URL = RETURN_MEDIA_AS_URL,
        RETURN_MEDIA_AS_BASE64_STRING = RETURN_MEDIA_AS_BASE64_STRING,
        EXTENDED_MEDIA_INFO = EXTENDED_MEDIA_INFO,
        MULTIPART_FORM_FIELDS_AS_JSON = MULTIPART_FORM_FIELDS_AS_JSON,
        
        MONGO1T_HOST = MONGO1T_HOST,
        MONGO1T_PORT = MONGO1T_PORT,
        MONGO1T_DBNAME = MONGO1T_DBNAME,
        MONGO1T_USERNAME = MONGO1T_USERNAME,
        MONGO1T_PASSWORD = MONGO1T_PASSWORD,
        MONGO1T_AUTH_SOURCE = MONGO1T_AUTH_SOURCE,
        
        MONGO_HOST = MONGO_HOST,
        MONGO_PORT = MONGO_PORT,
        MONGO_DBNAME = MONGO_DBNAME,
        MONGO_USERNAME = MONGO_USERNAME,
        MONGO_PASSWORD = MONGO_PASSWORD,
        MONGO_AUTH_SOURCE = MONGO_AUTH_SOURCE,

        SERVERS = SERVERS,
        X_DOMAINS = X_DOMAINS,
        X_HEADERS = X_HEADERS,
        JWT_KEY_URL = JWT_KEY_URL,
        JWT_AUDIENCES = JWT_AUDIENCES,
        JWT_SCOPE_CLAIM = JWT_SCOPE_CLAIM,
        JWT_TTL = JWT_TTL,
    )
    if os.getenv("XESTORE_MONGO_URI", ""):
        settings["MONGO1T_URI"] = MONGO1T_URI
        settings["MONGO_URI"] = MONGO_URI

    if os.getenv("XESTORE_MONGO_REPLICA_SET", ""):
        settings["MONGO_REPLICA_SET"] = MONGO_REPLICA_SET
        settings["MONGO1T_REPLICA_SET"] = MONGO1T_REPLICA_SET

    settings.update(overrides)
    return settings