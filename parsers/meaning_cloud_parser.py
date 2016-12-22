
from json_nlp_parser import JSONNlPParser

import json
from pprint import pprint

class MeaningCloudParser(JSONNlPParser):

    def __init__(self):
        print "#> Initing CortParser . .."
        self.root_str = None
        self.root_dict = None
        super(MeaningCloudParser, self).__init__(self)

    def load_data(self, json_str):

        if json_str is not None and len(json_str) > 0:
            self.root_str = super(MeaningCloudParser, self).save_data(json_str)

        if self.root_str is not None and len(json_str) > 0:
            self.root_dict = super(MeaningCloudParser, self).load_data(self.root_str)
            print " >1> self.root: " + str(self.root_dict)
        else:
            print " %% Don't have json_str or saved json_str"

    def save_data(self, json_str, needs_wrapper=False):
        self.root_str = super(MeaningCloudParser, self).save_data(json_str, needs_wrapper)
        print " >1----> self.root_str: " + str(self.root_str)

    def do_tests(self):

        print self.root_dict[u'token_list']

        test_node = super(MeaningCloudParser, self)._finditem(self.root_dict, u'token_list')
        print " test_node: " + str(test_node)

        test_node = super(MeaningCloudParser, self)._get_recursively(self.root_dict, u'affected_by_negation')
        print " test_node: " + str(test_node)

        test_node = super(MeaningCloudParser, self)._get_recursively(self.root_dict, u'iof_isPossessor')
        print " test_node: " + str(test_node)

        ## looking for such as in #49
        # "Sid" antecedent.iof_isAnaphora value(23) == the proform.id(23)
        # AND
        # "he"/"him" proform.isAnaphora value(19) = the antecedent.id(19)




# with open('data.json') as data_file:
#     data = json.load(data_file)

json1 = '{"a": { "b":1 }}'

mcp = MeaningCloudParser()
mcp.load_data(json1)

# "data/meaningCloud_output_json"

f = open('/Users/ryanpanos/Documents/code/nlp-parsers/data/meaningCloud_output_json/15_winograd.json', 'r')
mcp2 = MeaningCloudParser()
mcp2.load_data(f.read())


mcp2.do_tests()