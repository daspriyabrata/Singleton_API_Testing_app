#!/usr/bin/env python
import logging
import os
import json
from app_lib.apittest import ZomatoAPITest
from utils.config import config_parser
from utils.Singleton import ZOmato_API_Factory
from utils.test_case import test_case_parser


def main():
    # Create the singleton class to map all objects
    # Makes writing plugins easier
    api_factory = ZOmato_API_Factory()
    # Store the settings
    api_factory.settings = json.loads(config_parser(os.getcwd() + '/data/config.yml').replace("\'", "\""))
    # Create a logger
    format = "%(asctime)s: %(message)s"
    api_factory.log = logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    api_factory.test_cases = test_case_parser(os.getcwd() + '/data/test_case.yml')

    # The zomato api bot itself
    api_factory.test_runner = ZomatoAPITest(api_factory.settings, api_factory.test_cases)

    return api_factory


if __name__ == "__main__":
    zomato_api = main()
    zomato_api.test_runner.run()
