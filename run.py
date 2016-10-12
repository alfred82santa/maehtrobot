from maehtrobot.common import create_application
from maehtrobot import config

if __name__ == '__main__':

    app = create_application(config.ENVIRONMENT, config.CONFIG_NAME, config.CONFIG_PATH)
    app.run()