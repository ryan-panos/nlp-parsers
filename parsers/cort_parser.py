import collections
from xml_nlp_parser import XMLNlPParser
# from xml.etree.ElementTree import *
import xml.etree.ElementTree as ET

class CortParser(XMLNlPParser):

    def __init__(self):
        print "#> Initing CortParser . .."
        self.root_str = None
        self.root = None
        super(CortParser, self).__init__(self)

    ## NOT USED?
    def load_data(self, xml_str, needs_wrapper=False):
        # XMLNlPParser(self, xml_str)
        self.root = super(CortParser, self).load_data(xml_str, needs_wrapper)
        print " >1> self.root: " + str(self.root)

    def save_data(self, xml_str, needs_wrapper=False):
        # XMLNlPParser(self, xml_str)
        self.root_str = super(CortParser, self).save_data(xml_str, needs_wrapper)
        print " >1----> self.root_str: " + str(self.root_str)

    def build_matches(self):
        cnt = 1
        if hasattr(self, "root") and self.root is None and self.root_str is not None:
            self.root = ET.fromstring(self.root_str)
        else:
            print " ## ERR: root_str and root are both None ..." + str(self.root_str) + "| " + str(self.root)

        print " 2 self.root is " + str(self.root)


        all_entities = collections.OrderedDict()

        # for mention in self.root.iter('mention'):
        for mention in self.root.findall('mention'):
            cnt += 1
            if cnt % 1 == 0:
                # print str(cnt) + ": " + str(mention.attrib)
                if mention.attrib.get('entity', None) is not None:
                    # if mention.attrib.get('entity', None) is not None:
                    entity = mention.attrib.get('entity')
                    if all_entities.get(entity, None) is not None:
                        # if hasattr(all_entities, entity):
                        all_entities[entity].append(mention)  ##Todo: consider a more useful structure?
                    else:
                        all_entities[entity] = [mention]
                else:
                    #print " NO entity? " + str(mention.attrib.get('entity'))
                    pass


        for key, mention_ls in all_entities.iteritems():
            print " ___________ \n Entity: " + str(key)
            for mention in mention_ls:
                print "mention.text: " + str(mention.text)


        pass




xml1 = "<x> hamster </x>"
xml2 = "<x> hamster <y>fred </y></x>"
xml3 = "<x> hamster <mention>of death</mention></x>"
xml4 = "<x> hamster <mention>of death & crap </mention></x>"

def test_cort1():
    cp = CortParser()


    print " GONNA READ "

    f = open('/Users/ryanpanos/Documents/code/nlp-parsers/data/winograd_cort_plain.xml', 'r')  # MAKE THIS RELATIVE!
    # print f.read()
    # cp.load_data(f.read(), needs_wrapper=True)
    cp.save_data(f.read(), needs_wrapper=True)
    # cp.save_data(xml4)

    cp.build_matches()


test_cort1()