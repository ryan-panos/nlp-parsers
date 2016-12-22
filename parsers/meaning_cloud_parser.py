
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

        # from https://www.meaningcloud.com/developer/lemmatization-pos-parsing/doc/2.0/response
        # Observations
        # token_list(s) can be a list of tokens.  A token might be a sentance, phrase or word
        # for co-ref, we obv dont care about sentances!
        # phase can be "the dog" and it will have a sub token_list with "dog"
        #
        # CONCERNs: phase can be "which" and sub token_list can be some analysis on which?!?!
        #    So one word can be a phrase and its still not the leaf, at least in example 102
        # docs say "word" is a type but it is not in example 102 - probably its sentance, phrase and **word types**
        #
        # syntactic_tree_relation_list is the key!  Every token seems to have these and they tie this token to
        # the antecendant or proform
        #
        # EXAMPLE of coref
        # in ex102:   "The dog chased the cat, which ran up a tree."  "It waited at the bottom."
        # "Which" has id=27 and also has
        # "syntactic_tree_relation_list": [
        #         {
        #             "type": "isAnaphora",
        #             "id": "25"
        #         }
        #     ],
        #   and "the cat" has id=25 and also has:
        #
        # "syntactic_tree_relation_list": [
        #                                     {
        #                                         "type": "isSubject",
        #                                         "id": "8"
        #                                     },
        #                                     {
        #                                         "type": "isDirectObject",
        #                                         "id": "3"
        #                                     },
        #                                     {
        #                                         "type": "iof_isNonRestrictiveApposition",
        #                                         "id": "29"
        #                                     },
        #                                     {
        #                                         "type": "iof_isAnaphora",
        #                                         "id": "27"
        #                                     },
        #                                     {
        #                                         "type": "iof_isAnaphora",
        #                                         "id": "32"
        #                                     }
        #                                 ],
        # #
        #
        #  Note 27 pertains to "which" and "32" pertains to "it" in the next sentance
        #






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