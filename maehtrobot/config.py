import os


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(BASE_PATH, 'data')
LOGS_BASE_PATH = os.path.join(DATA_PATH, 'logs')
CONFIG_PATH = os.path.join(BASE_PATH, 'config')

ENVIRONMENT = "development"
CONFIG_NAME = "maehtrobot"
