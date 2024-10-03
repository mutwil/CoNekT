"""
Configuration of the website and database.

Copy this file to config.py and change the settings accordingly
"""

import os
import tempfile

basedir = os.getcwd()

# Flask settings, make sure to set the SECRET_KEY and turn DEBUG and TESTING to False for production
DEBUG = False
TESTING = True
WTF_CSRF_ENABLED = False

SECRET_KEY = "DragonsLiveHere"

# Login settings + admin account
LOGIN_ENABLED = True
ADMIN_PASSWORD = "admin"
ADMIN_EMAIL = "admin@web.com"


# Database settings, database location and path to migration scripts
# Will use in memory db for testing
SQLALCHEMY_DATABASE_URI = "sqlite://"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "migration")
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Settings for the FTP/bulk data
PLANET_FTP_DATA = tempfile.mkdtemp()

# Settings for Cache
CACHE_TYPE = "null"
CACHE_DEFAULT_TIMEOUT = 600
CACHE_THRESHOLD = 10000
CACHE_NO_NULL_WARNING = True

# Whooshee settings
WHOOSHEE_DIR = tempfile.mkdtemp()
WHOOSHEE_MIN_STRING_LEN = 3
WHOOSHEE_WRITER_TIMEOUT = 2
WHOOSHEE_MEMORY_STORAGE = False
WHOOSHEE_ENABLE_INDEXING = True

# Minify pages when debug is off
MINIFY_PAGE = not DEBUG

TMP_DIR = tempfile.mkdtemp()

# BLAST settings
BLAST_ENABLED = False
BLAST_TMP_DIR = tempfile.mkdtemp()

BLASTP_PATH = "D:/blast/bin/blastp.exe"
BLASTP_DB_PATH = "D:/blast/db/ath_db"
BLASTN_PATH = "D:/blast/bin/blastn.exe"
BLASTN_DB_PATH = "D:/blast/db/ath_cds_db"

BLASTP_CMD = (
    BLASTP_PATH
    + " -db "
    + BLASTP_DB_PATH
    + " -query <IN> -out <OUT> -outfmt 6 -num_threads 1"
)
BLASTN_CMD = (
    BLASTN_PATH
    + " -db "
    + BLASTN_DB_PATH
    + " -query <IN> -out <OUT> -outfmt 6 -num_threads 1"
)

# Debug settings
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Twitter Handle
TWITTER_HANDLE = None
