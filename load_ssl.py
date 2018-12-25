# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import yaml
import os
from hostinger import Hostinger

def load_config():
    with open(".env.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
            if os.environ.get('HOSTINGER_USER'):
                config["hostinger"]['username'] = os.environ.get('HOSTINGER_USER')
            if os.environ.get('HOSTINGER_PASSWORD'):
                config["hostinger"]['hosting_id'] = os.environ.get('HOSTINGER_PASSWORD')
            if os.environ.get('HOSTINGER_ID'):
                config["hostinger"]['password'] = os.environ.get('HOSTINGER_PASSWORD')
            return config
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    config = load_config()
    h = Hostinger(config)
    h.load_ssl()
