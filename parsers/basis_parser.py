
from json_nlp_parser import JSONNlPParser

DATA_DIR = '/Users/ryanpanos/Documents/code/nlp-parsers/data/'

class BasisParser(JSONNlPParser):

    def __init__(self):
        # print "#> Initing CortParser . .."
        self.root_str = None
        self.root_dict = None
        self._entities = None

        # self.converted_sentance_w_proform = None
        # self.converted_sentance_only_ent = None
        # self.scorez = None
        super(BasisParser, self).__init__(self)

    def _load_entities(self):
        
        if self._entities is not None:
            print "## Entities already loaded "
            return
        elif self.root_dict is None:
            print "%% ROOT NOT LOADED in BasisParser s7689h"
            return
        elif "entities" not in self.root_dict:
            print "%% ROOT not None but no entities found"

        self._entities = self.root_dict["entities"]
        return self._entities
        
        
        
        
    def load_data(self, json_str):

        if json_str is not None and len(json_str) > 0:
            self.root_str = super(BasisParser, self).save_data(json_str)

        if self.root_str is not None and len(json_str) > 0:
            self.root_dict = super(BasisParser, self).load_data(self.root_str)
            # print " > 1 > self.root: " + str(self.root_dict)
            self._load_entities()
        else:
            print " %% Don't have json_str or saved json_str"

    def save_data(self, json_str, needs_wrapper=False):
        self.root_str = super(BasisParser, self).save_data(json_str, needs_wrapper)
        print " >1----> self.root_str: " + str(self.root_str)
       
    


    def get_entity_node(self, normalized_str):
        if self._entities is None:
            if self._load_entities() is None:
                return None

        ## Todo - make a version of _finditem that only searches objects in lists - nothing deeper
        return super(BasisParser, self)._find_in_list(self._entities, "normalized", normalized_str)



## KEY ASSUMPTION: all the other servies will be given in an easy to digest format like the below
#   THEREFORE the parser will "try" to find the various services and populate a
#

entity_example_output = {
  "entities": [
    {
      "type": "PERSON",
      "mention": "Bill Murray",
      "normalized": "Bill Murray",
      "count": 1,
      "entityId": "Q29250"
    },
    {
      "type": "PRODUCT",
      "mention": "Ghostbusters",
      "normalized": "Ghostbusters",
      "count": 1,
      "entityId": "Q108745"
    },
    {
      "type": "TITLE",
      "mention": "Dr.",
      "normalized": "Dr.",
      "count": 1,
      "entityId": "T2"
    },
    {
      "type": "PERSON",
      "mention": "Peter Venkman",
      "normalized": "Peter Venkman",
      "count": 1,
      "entityId": "Q2483011"
    },
    {
      "type": "LOCATION",
      "mention": "Boston",
      "normalized": "Boston",
      "count": 1,
      "entityId": "Q100"
    },
    {
      "type": "IDENTIFIER:URL",
      "mention": "http://dlvr.it/BnsFfS",
      "normalized": "http://dlvr.it/BnsFfS",
      "count": 1,
      "entityId": "T5"
    }
  ],
  "responseHeaders": {
    "date": "Fri, 21 Oct 2016 17:46:30 GMT, Fri, 21 Oct 2016 17:46:31 GMT",
    "content-type": "application/json",
    "x-rosetteapi-request-id": "1015dde9-9e79-421e-bc4d-028a8b45a2c0",
    "x-rosetteapi-processedlanguage": "eng",
    "connection": "close",
    "server": "Jetty(9.2.17.v20160517)"
  }
}


def test_basis():
    source = DATA_DIR + 'winograd.csv'


f = open(DATA_DIR + 'NER/5_basis-ner.json', 'r')
basis_p1=BasisParser()
basis_p1.load_data(f.read())

# TODO: does normalized mean . .  lower case when appropriate?

ner_node1 = basis_p1.get_entity_node("LAS CRUCES")
print " GOT ner_node1: " + str(ner_node1)

ner_node2 = basis_p1.get_entity_node("CRAP")
print " This should be None: " + str(ner_node2)