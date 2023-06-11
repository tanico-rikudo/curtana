from logging import config, getLogger
import yaml

class EdinetLogger:
    def __init__(self):
        pass

    @classmethod
    def get_loggger(cls):
        cls.set_logger()
        logger = getLogger('edinetLogger')
        return logger

    @classmethod
    def set_logger(cls):
        with open("/opt/app/ini/log_config.yaml") as f:
            read_data = f.read()
            yaml_data = yaml.safe_load(read_data)
            config.dictConfig(yaml_data)

