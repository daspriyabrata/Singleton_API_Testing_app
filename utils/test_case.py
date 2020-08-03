from utils.yml_reader import read_yaml
from benedict import benedict
import logging

logger = logging.getLogger(__name__)


def test_case_parser(test_case_file_path):
    test_cases = read_yaml(test_case_file_path)
    return test_cases


class TestRunner:

    @staticmethod
    def status_code(response, **kwargs):
        try:
            assert response.status_code == int(kwargs.get('status_code'))
            return 'Passed'
        except AssertionError as e:
            logger.info(e)
            return 'Failed', 'Status Code is: ' + str(response.status_code)
        except TypeError as e:
            logger.info(e)
            return 'Failed', 'Type Error' + str(type(response.status_code)) + ' and ' + \
                   str(type(kwargs.get('status_code'))) + ' are not same.'

    @staticmethod
    def field_present(response, **kwargs):
        _resp_str = benedict(response.json())
        try:
            assert kwargs.get('field_name') in _resp_str
            return 'Passed'
        except KeyError:
            logger.info(kwargs.get('field_name') + ' is not present.')
            return 'Failed', kwargs.get('field_name') + ' is not present.'

    @staticmethod
    def field_value(response, **kwargs):
        _resp_json = benedict(response.json())
        _assert_field = list(kwargs.keys())[1]
        _assert_value = kwargs.get(_assert_field)
        try:
            assert _resp_json[_assert_field] == _assert_value
            return 'Passed'
        except KeyError:
            logger.info(_assert_field + ' is not present.')
            return 'Failed', _assert_field + ' is not present.'
        except ValueError:
            logger.info(_assert_field + 'does not have value as' + _assert_value)
            return 'Faied', _assert_field + 'does not have value as' + _assert_value

    @staticmethod
    def performance(response, **kwargs):
        try:
            assert response.elapsed.total_seconds() < float(kwargs.get('time_limit'))
            return 'Passed'
        except AssertionError as e:
            logger.info(e)
            return 'Failed', 'Time Taken is: ' + str(response.elapsed.total_seconds())
        except TypeError as e:
            logger.info(e)
            return 'Failed', 'Type Error' + str(type(response.status_code)) + ' and ' + \
                   str(type(kwargs.get('status_code'))) + ' are not same.'

    @staticmethod
    def header_params_check(response, **kwargs):
        header_param = list(kwargs.keys())[1]
        try:
            assert response.headers[header_param] == kwargs.get(header_param)
            return 'Passed'
        except AssertionError as e:
            logger.info(e)
            return 'Failed', 'Header Param did not match'
        except TypeError as e:
            logger.info(e)
            return 'Failed', 'Type Error' + str(type(response.status_code)) + ' and ' + \
                   str(type(kwargs.get('status_code'))) + ' are not same.'

