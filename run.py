import logging
import sys
import os

BASE_URL = os.path.abspath(os.path.dirname(__file__))

from app import create_app

# config_name = "development"
config_name = os.getenv('APP_SETTINGS')
if config_name is None:
    config_name == "development"
app = create_app(config_name)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(debug=True)
