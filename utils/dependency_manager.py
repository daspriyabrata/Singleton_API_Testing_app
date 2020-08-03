import os
import json
from benedict import benedict


class DependencyManager:

    def __init__(self, _tc_details):
        self._tc_details = _tc_details
        self._dependent_api_name = self._tc_details.get('depedent_api')
        self._dependent_test_case = self._tc_details.get('dependent_test_case')
        self._dependant_component = self._tc_details.get('dependant_component')
        self.depending_fields = self._tc_details[self._dependant_component]

    def get_dependent_component(self):
        required_json = os.getcwd() + '/RESPONSE_JSON/' + self._dependent_api_name + '/' + self._dependent_test_case + '.json'
        with open(required_json, 'r') as file:
            data = json.load(file)
            file.close()
        json_data = benedict(data)
        for k, v in self.depending_fields.items():
            self.depending_fields.update({k: json_data[v]})
        return self.depending_fields
