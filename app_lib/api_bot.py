import logging
import datetime
from utils.http_request import HttpRequests
from utils.test_case import TestRunner
from utils.json_writer import ResponseJsonWriter
from utils.dependency_manager import DependencyManager
from HTML_Report.html_reports import HtmlReport

logger = logging.getLogger(__name__)


class Zomato_API_BOT:
    def __init__(self, settings, test_cases):
        self._settings = settings
        self._test_cases = test_cases
        self._http_request_generator = HttpRequests(self._settings['base_url'], self._settings['user_key'])
        self.report = {}

    def run(self):
        self.report['start_time'] = datetime.datetime.utcnow()
        _json_registry = ResponseJsonWriter('RESPONSE_JSON')
        self.report['test_cases'] = []
        for api in list(self._test_cases.keys()):
            _json_registry.create_response_repository(api)
            print('Test run started for ' + api)
            logger.debug('Testing for {api} api')
            for test_case in list(self._test_cases[api].keys()):
                _test_case_id = test_case
                _case_level_report = {'summary': api + ' ' + _test_case_id}
                test_details = self._test_cases[api][_test_case_id]
                _test_runner = getattr(TestRunner, test_details['tc_type'])
                if test_details.get('is_dependent'):
                    _dependency_manager = DependencyManager(test_details)
                    query_params = _dependency_manager.get_dependent_component()
                elif test_details.get('query_params'):
                    query_params = test_details.get('query_params')
                else:
                    query_params = None
                _response = self._http_request_generator.get_details(api, query_params)
                _resp_json_loc = _json_registry.write_response_json_files(_response, _test_case_id)
                _case_level_report.update({'response_json_loc': _resp_json_loc})
                result = _test_runner(_response, **test_details)
                if result == 'Passed':
                    _case_level_report['test_detail'] = test_details
                    _case_level_report['result'] = 'Pass'
                    print(str(test_details) + ' Passed')
                else:
                    _case_level_report['failure_reason'] = result[1]
                    _case_level_report['result'] = result[0]
                    print(str(test_details) + result[0] + ' with reason ' + result[1])
                self.report['test_cases'].append(_case_level_report)
                _response.close()
        self.report['end_time'] = datetime.datetime.utcnow()
        print(HtmlReport.report_builder(self.report))
        print("Total time elapsed {}".format(str(self.report['end_time'] - self.report['start_time'])))
        print('Test Run Finished')
