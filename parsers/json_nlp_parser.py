
from base_parser import BaseParser

import json
from pprint import pprint



class JSONNlPParser(BaseParser):

    def __init__(self, child):
        print "#> Initing JSONNlPParser . .."
        ## Todo : call parent just in case?

    def _finditem(self, obj, key):
        if key in obj: return obj[key]
        if isinstance(obj, list):
            for sub_obj in obj:
                return self._finditem(sub_obj, key)
        for k, v in obj.items():
            if isinstance(v, dict):
                item = self._finditem(v, key)
                if item is not None:
                    return item

    def _get_recursively(self, search_dict, field):
        """
        Takes a dict with nested lists and dicts,
        and searches all dicts for a key of the field
        provided.
        """
        fields_found = []

        for key, value in search_dict.iteritems():

            if key == field:
                fields_found.append(value)

            elif isinstance(value, dict):
                results = self._get_recursively(value, field)
                for result in results:
                    fields_found.append(result)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = self._get_recursively(item, field)
                        for another_result in more_results:
                            fields_found.append(another_result)

        return fields_found


    def load_json_file(self, json_file_name):

        with open(json_file_name) as data_file:
            data = json.load(data_file)
            return data

    def load_data(self, json_str, needs_wrapper=False):
        print " ## Gonna load " + json_str
        #todo need error checking?

        ## TODO: decode unicode here!!??!!?

        data = json.loads(json_str)
        # data.close()
        return data


    def save_data(self, json_str, needs_wrapper=False):

        # do JSON checking here?

        return json_str




    def open_data(self, json_file_name, needs_wrapper=False):

        with open(json_file_name) as json_str:

            # No pre work at all?
            return self.save_data(json_str)

        print " ## Cant open " + json_file_name
