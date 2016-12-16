
from base_parser import BaseParser
# from xml.etree.ElementTree import *
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

class XMLNlPParser(BaseParser):

    def __init__(self, child):
        print "#> Initing XMLParser . .."


    def load_data(self, xml_str, needs_wrapper=False):

        # TODO: store xml_str as well?

        if needs_wrapper:
            xml_str = "<root>" + xml_str + "</root>"
            # print " xml_str: " + str(xml_str)
        xml_str = xml_str.encode('utf-8')
        print "#> doing XMLParser.load_data . .. " + str(xml_str[:200])

        try:
            root = ET.fromstring(xml_str)
            print " >0> " + str(root)
            return root
        except ParseError as e:
            formatted_e = str(e)
            line = int(formatted_e[formatted_e.find("line ") + 5: formatted_e.find(",")])
            column = int(formatted_e[formatted_e.find("column ") + 7:])
            split_str = xml_str.split("\n")
            print "{}\n{}^".format(split_str[line - 1], len(split_str[line - 1][0:column]) * "-")

        # self.root = fromstring(xml_str)
        # BaseParser.load_data(xml_str)  # Moot?

    def save_data(self, xml_str, needs_wrapper=False):
        if needs_wrapper:
            xml_str = "<root>" + xml_str + "</root>"

        ## THIS is required but I am guessing other encoding will be needed??
        xml_str_encode = xml_str.replace('&','&amp;') # .encode('')  #  utf-8  string_escape  ascii quopri  .replace('&','&amp;')

        return xml_str_encode
