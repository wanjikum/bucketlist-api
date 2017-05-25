import logging
import sys
import os

BASE_URL = os.path.abspath(os.path.dirname(__file__))

from app import create_app

config_name = "development"
# config_name = os.getenv('APP_SETTINGS')

app = create_app(config_name)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(debug=True)
