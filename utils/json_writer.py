import os
import json
import shutil


class ResponseJsonWriter:

    def __init__(self, _folder_name):
        self._api_collection = None
        self._fp = None
        self._path = os.getcwd()+'/'+_folder_name
        if os.path.exists(self._path):
            shutil.rmtree(self._path)

    def create_response_repository(self, _api_name):
        self._api_collection = self._path+'/'+_api_name
        self._fp = _api_name
        if os.path.exists(self._api_collection):
            os.rmdir(self._api_collection)
        os.makedirs(self._api_collection)

    def write_response_json_files(self, _response, _test_case_id):
        file_path = self._api_collection+'/'+_test_case_id+'.json'
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'x') as json_file:
            json.dump(_response.json(), json_file, indent=4)
            json_file.close()
        return self._fp+'/'+_test_case_id+'.json'


