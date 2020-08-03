import configparser
from utils.yml_reader import read_yaml


def config_parser(config_file_path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = read_yaml(config_file_path)
    return config['DEFAULT']['test_config']
