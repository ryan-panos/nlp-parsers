
from json_nlp_parser import JSONNlPParser

import json
from pprint import pprint

DATA_DIR = '/Users/ryanpanos/Documents/code/nlp-parsers/data/'

class MeaningCloudParser(JSONNlPParser):

    def __init__(self):
        # print "#> Initing CortParser . .."
        self.root_str = None
        self.root_dict = None

        self.converted_sentance_w_proform = None
        self.converted_sentance_only_ent = None
        self.scorez = None
        super(MeaningCloudParser, self).__init__(self)

    def load_data(self, json_str):

        if json_str is not None and len(json_str) > 0:
            self.root_str = super(MeaningCloudParser, self).save_data(json_str)

        if self.root_str is not None and len(json_str) > 0:
            self.root_dict = super(MeaningCloudParser, self).load_data(self.root_str)
            # print " > 1 > self.root: " + str(self.root_dict)
        else:
            print " %% Don't have json_str or saved json_str"

    def save_data(self, json_str, needs_wrapper=False):
        self.root_str = super(MeaningCloudParser, self).save_data(json_str, needs_wrapper)
        print " >1----> self.root_str: " + str(self.root_str)

    def do_tests(self):

        print self.root_dict[u'token_list']

        test_node = super(MeaningCloudParser, self)._finditem(self.root_dict, u'token_list')
        print " test_node: " + str(test_node)

        test_node = super(MeaningCloudParser, self)._finditem(self.root_dict, 'token_list')
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


        ## Coref Solution idea #1

        # use dict_digger to recursiveley search each layer for needed values
        #     If "has token list"
        #         for each member of token list
        #             has iof_isAnaphora?
        #                 add relavent data to an obj
        #                 add obj to a list of iof_isAnaphora
        #             has isAnaphora?
        #                 add relavent data to an obj
        #                 add obj to a list_of_isAnaphora

        # foreach list_of_iof_isAnaphora
        #     find ALL appropriate

    def _get_syntactic_tree_relation_ids_ls(self, token_obj, sought_property):
        # if hasattr(token_obj, "syntactic_tree_relation_list"):
        if u'syntactic_tree_relation_list' in token_obj:
            # print ' ------  FOUND syntactic_tree_relation_list: ' + str(token_obj[u'syntactic_tree_relation_list'])

            ids_ls = []
            for syn_rel_obj in token_obj[u'syntactic_tree_relation_list']:
                if u'type' in syn_rel_obj:
                    if syn_rel_obj[u'type'] == sought_property:
                        if u'id' in syn_rel_obj:
                            ids_ls.append(syn_rel_obj[u'id'])
                        else:
                            print "%% BROKEN JSON: NO id in syn_rel_obj??"
                else:
                    print "%% BROKEN JSON: NO type in syn_rel_obj??"

            return ids_ls
        else:
            # print ">> syntactic_tree_relation_list missing: " + str(token_obj) # NORMAL AT MANY NODES!
            return None

    # todo - possiblyt make a wrapper "public" version that does not expect an empty the_prop_ls_dict
    def _get_all_props_ls(self, token_ls, prop_ls, the_prop_ls_dict):

        # if prop_ls is empty, return None

        if token_ls is None or len(token_ls) < 1:
            print " %% token_ls is empty?"
            return
        else:
            for token_obj in token_ls:

                #TEMP:
                # print " WIll examine: " + str(token_obj)

                for prop in prop_ls:
                    syn_ls = self._get_syntactic_tree_relation_ids_ls(token_obj, prop)
                    if syn_ls is not None and len(syn_ls) > 0:

                        ## take note of "form" and other data in this token_obj!
                        syn_ls_dict = {
                           u'syn_ls': syn_ls
                        }

                        print " syn_ls len : " + str(len(syn_ls))

                        if u'form' in token_obj: # could there be other ways they store "the word?"
                            syn_ls_dict[u'form'] = token_obj[u'form']
                        if u'id' in token_obj:
                            syn_ls_dict[u'id'] = token_obj[u'id']
                        if u'inip' in token_obj:
                            syn_ls_dict[u'inip'] = token_obj[u'inip']  # initial position!

                        if prop in the_prop_ls_dict:
                            the_prop_ls_dict[prop].append(syn_ls_dict)
                        else:
                            the_prop_ls_dict[prop] = [syn_ls_dict] # need to prepare for many isAnaphora or whatever!

                if u'token_list' in token_obj:
                    # print " GOING SUB . .."
                    self._get_all_props_ls(token_obj[u'token_list'], prop_ls, the_prop_ls_dict)
                # else:
                #     print " NO token_list? " + str(token_obj)

            return the_prop_ls_dict



    def test_prop_getter(self):
        prop_ls = [u'iof_isAnaphora', u'isAnaphora']
        the_prop_ls_dict = {} #todo - rename?
        if u'token_list' in self.root_dict:
            the_prop_ls_dict = self._get_all_props_ls(self.root_dict[u'token_list'], prop_ls, the_prop_ls_dict)
        else:
            print " No token_list in root?"
            for key, node in self.root_dict.iteritems():
                print " FOUND: " + key
                print " IS " + str(node)


        # print " >> the_prop_ls_dict: " + str(the_prop_ls_dict)
    def _get_antecdenat_str(self, of_isAnaphora_ls, eid):

        poss_ls = filter(lambda ent_node: int(ent_node[u'id']) == eid, of_isAnaphora_ls)
        if poss_ls is None or len(poss_ls) == 0:
            print " %% no entities fitting in " + str(of_isAnaphora_ls) + " |+| " + str(eid)
            return None

        else:
            print "   FOUND:" + str(poss_ls[0][u'form'])
            return poss_ls[0][u'form']

            #(item for item in of_isAnaphora_ls if int(item[u'id']) == eid).next()


    def find_swaps(self, original_input_str):

        prop_ls = [u'iof_isAnaphora', u'isAnaphora']
        the_prop_ls_dict = {}  # todo - rename?
        if u'token_list' in self.root_dict:

            the_prop_ls_dict = self._get_all_props_ls(self.root_dict[u'token_list'], prop_ls, the_prop_ls_dict)

            # the_prop_ls_dict['isAnaphora'] = the_prop_ls_dict['isAnaphora'].sort(key=lambda x: (  int(x[u'inip']),
            #                                                                             print str(x[u'inip'])))  # , reverse=True

            if 'isAnaphora' not in the_prop_ls_dict or len(the_prop_ls_dict['isAnaphora']) == 0:
                print " %% No isAnaphora for " + original_input_str
                return

            # sort by starting position so that we can accumulate the offset from left to right
            sorted_proforms = sorted(the_prop_ls_dict['isAnaphora'], key=lambda k: int(k[u'inip']))

            print " The Entities: " + str(the_prop_ls_dict[u'iof_isAnaphora'])
            print " The Proforms: " + str(sorted_proforms)

            START_TAG_A = '<span eid='
            START_TAG_B = ' class="pronoun_insert">'
            END_TAG = '</span>'
            converted_w_prfm_html_str = original_input_str
            converted_w_ent_only_str = original_input_str
            offset_w_prfm = 0
            offset_ent_only = 0
            missing_cnt = 0
            for proform_node in sorted_proforms:
                ent_id_ls = proform_node[u'syn_ls']

                if len(ent_id_ls) > 1:
                    print " ## MORE THAN ONE ENTITY?  HOPEFULLY SAME VALUE!  TAKING TOP "
                    ent_id_str = str(ent_id_ls[0])
                elif len(ent_id_ls) == 1:
                    ent_id_str = str(ent_id_ls[0])
                else:
                    print " >> NO ENTITIY ID FOR " + str(proform_node[u'syn_ls'])
                    continue



                curr_pos_w_prfm = int(proform_node[u'inip']) + offset_w_prfm
                end_pos_w_prfm = int(proform_node[u'inip']) + offset_w_prfm + len(proform_node[u'form'])

                curr_pos_ent_only = int(proform_node[u'inip']) + offset_ent_only
                end_pos_ent_only = int(proform_node[u'inip']) + offset_ent_only + len(proform_node[u'form'])


                entity_insert_str = self._get_antecdenat_str(the_prop_ls_dict[u'iof_isAnaphora'], int(ent_id_str))
                if entity_insert_str is None:
                    entity_insert_str = "[MISSING]"
                    missing_cnt += 1
                    print " ***** MISSING *****" # never happens in meaning cloud?

                new_pronoun_insert_str = START_TAG_A + ent_id_str + START_TAG_B + proform_node[u'form'] + "\\" + entity_insert_str + END_TAG
                print " new_pronoun_insert_str: " + new_pronoun_insert_str

                new_ent_only_insert_str = entity_insert_str

                converted_w_prfm_html_str = converted_w_prfm_html_str[:curr_pos_w_prfm] + new_pronoun_insert_str + converted_w_prfm_html_str[end_pos_w_prfm:]
                converted_w_ent_only_str = converted_w_ent_only_str[:curr_pos_ent_only] + new_ent_only_insert_str + converted_w_ent_only_str[end_pos_ent_only:]

                offset_w_prfm = offset_w_prfm + len(new_pronoun_insert_str) - len(proform_node[u'form'])
                offset_ent_only = offset_ent_only + len(new_ent_only_insert_str) - len(proform_node[u'form'])

            print ">> NOW: " + converted_w_ent_only_str
            self.converted_sentance_w_proform = converted_w_prfm_html_str
            self.converted_sentance_only_ent = converted_w_ent_only_str
            self.scorez = {
                "missing_perc": float(missing_cnt/float(len(sorted_proforms)))
            }
            print "missing_cnt :" + str(missing_cnt)

        else:
            print " No token_list in root?"


    def has_antecedent_proform_match(self, proform, antecedent, doSwapOutputs=False):
        filename = DATA_DIR + "the_swaps.txt"
        swap_target = open(filename, 'w')

        prop_ls = [u'iof_isAnaphora', u'isAnaphora']
        the_prop_ls_dict = {}  # todo - rename?
        if u'token_list' in self.root_dict:
            the_prop_ls_dict = self._get_all_props_ls(self.root_dict[u'token_list'], prop_ls, the_prop_ls_dict)
        else:
            print " No token_list in root?"

        if the_prop_ls_dict is None or len(the_prop_ls_dict) < 1 or u'iof_isAnaphora' not in the_prop_ls_dict:
            print " ERROR NO u'iof_isAnaphora', u'isAnaphora'?? ---- looping : " + str(the_prop_ls_dict)
            # print ' from: ' + str(self.root_dict[u'token_list'])
            return
        found_one_success = 0
        sol_antecedent = None
        sol_proform = None
        for poss_antecedent in the_prop_ls_dict[u'iof_isAnaphora']:
            if str(poss_antecedent[u'form']) == antecedent:
                # print " antecedent match possible : " + str(poss_antecedent)
                proform_id_ls = []
                antecedent_id = poss_antecedent[u'id'] # still unicode
                for id in poss_antecedent[u'syn_ls']:
                    proform_id_ls.append(str(id))

                for poss_proform_node in the_prop_ls_dict[u'isAnaphora']:
                    criteria_cnt = 0
                    # does this node have the same id as in proform_id_ls?
                    if str(poss_proform_node[u'id']) in proform_id_ls:
                        criteria_cnt += 1
                        print " proform id is in antcendant id list!" + str(poss_proform_node[u'id'])

                    # also does antecedent_id exist in this syn_ls?
                    if antecedent_id in poss_proform_node[u'syn_ls']:
                        criteria_cnt += 1
                        print " antecedant id is in antcendant syn_ls! " + str(antecedent_id)

                    # is this where we know? - DEPENDANT ON KNOWING antecedent here!
                    # if criteria_cnt == 2:
                        # try to swa here?



                    if str(poss_proform_node[u'form']).replace('\.','').lower() == proform.lower().replace('."',''):
                        criteria_cnt += 1
                        print " And proform matches!! " + str(proform)
                    else:
                        print " Maybe missing proform match :" + str(poss_proform_node[u'form']) + "|=|" + proform + "|"
                        print " >> **NOT** found solution " + str(poss_antecedent) + "|=|" + str(poss_proform_node)

                    print " criteria_cnt = " + str(criteria_cnt)

                    if criteria_cnt != 3:
                        # print " FAIL? "
                        pass
                    elif criteria_cnt == 3:
                        print " SUCCEED! "
                        found_one_success = True
                        #save it some how?
                        sol_antecedent = poss_antecedent
                        sol_proform = poss_proform_node
                    # else:
                    #     print " UNKNOWN STATUS "

        if found_one_success:
            print " >> found solution " + str(sol_antecedent) + "|=|" + str(sol_proform)
            return True
        else:
            print "Didnt find match? "

            return False




def test_winograd(print_solution=False):

    source = DATA_DIR + 'winograd.csv'
    # source = '/Users/ryanpanos/Documents/code/nlp-parsers/data/winograd.csv'
            # /Users/ryanpanos/Documents/code/nlp-parsers/data
    # for line in
    with open(source, "r") as ins:
        # array = []
        total_success = 0
        tried_cnt = 0
        for idx, line in enumerate(ins):
            line_ls = line.split('","')
            proform = line_ls[1]
            antecedent = line_ls[2].replace('\"','').replace('\n','')
            sentance = line_ls[0].replace('\"','')
            # print " proform:" + str(proform) + "|"
            # print " anaform:" + str(Antecedent) + "|"

            if antecedent != 'Antecedent': # skip line # 1
                ans_file = 'meaningCloud_output_json/' + str(idx+1) + '_winograd.json'
                f = open(DATA_DIR + ans_file, 'r')
                mcp = MeaningCloudParser() ## just once?
                mcp.load_data(f.read())
                tried_cnt += 1
                # mcp.test_prop_getter()
                if print_solution:
                    print "\n FROM: " + sentance
                    print " HOPING FOR: " + proform + " = " + antecedent

                if mcp.has_antecedent_proform_match(proform, antecedent):
                    total_success += 1

        print "\n\n >> Found " + str(total_success) + " out of " + str(tried_cnt)
    print " DONE " + source


def write_dir_subs(dir_str, print_solution=False):
    import os
    print(os.path.isdir(dir_str))


def do_winograd_subs(print_solution=False):

    SOL_HEAD_HTML = '<div class="mc_sol"><p>'
    SOL_TAIL_HTML = '</div>'
    SCR_HEAD_HTML = '<span class="mc_scr">'
    SCR_TAIL_HTML = '</span>'
    sol_html = ""
    simple_html = ""
    source = DATA_DIR + 'winograd.csv'
    # source = '/Users/ryanpanos/Documents/code/nlp-parsers/data/winograd.csv'
            # /Users/ryanpanos/Documents/code/nlp-parsers/data
    # for line in
    with open(source, "r") as ins:
        # array = []
        total_success = 0
        tried_cnt = 0
        for idx, line in enumerate(ins):

            # this just breaks up input file ...
            line_ls = line.split('","')
            proform = line_ls[1]
            antecedent = line_ls[2].replace('\"','').replace('\n','')
            sentance = line_ls[0].replace('\"','')
            # print " proform:" + str(proform) + "|"
            # print " anaform:" + str(Antecedent) + "|"

            #  each input line should already have an output file of "all" the info but in the
            #  winograd corpus, there is only one EXPEPECTED pairing of antecendant and proform
            if antecedent != 'Antecedent': # skip line # 1
                ans_file = 'meaningCloud_output_json/' + str(idx+1) + '_winograd.json'
                f = open(DATA_DIR + ans_file, 'r')

                mcp = MeaningCloudParser() ## just once?
                mcp.load_data(f.read())

                # expect a score on return?  Or maybe the converted? BOTH? They could also be stored in the object
                mcp.find_swaps(sentance)
                score_txt = '? score'
                if mcp.converted_sentance_w_proform is not None:
                    if mcp.scorez is not None and "missing_perc" in mcp.scorez:
                        score_txt = "score: " + str(mcp.scorez["missing_perc"])
                    sol_html += SOL_HEAD_HTML + mcp.converted_sentance_w_proform + SCR_HEAD_HTML + score_txt + SCR_TAIL_HTML + \
                                SOL_TAIL_HTML

                if mcp.converted_sentance_only_ent is not None:
                    simple_html += mcp.converted_sentance_only_ent + "  "

                # tried_cnt += 1
                # # mcp.test_prop_getter()
                # if print_solution:
                #     print "\n FROM: " + sentance
                #     print " HOPING FOR: " + proform + " = " + antecedent
                #
                # if mcp.has_antecedent_proform_match(proform, antecedent):
                #     total_success += 1

        print "\n\n >> Found " + str(total_success) + " out of " + str(tried_cnt)
    print " DONE " + source + "\n\n"
    print sol_html
    print "\n\n" + simple_html


# with open('data.json') as data_file:
#     data = json.load(data_file)

json1 = '{"a": { "b":1 }}'

# mcp = MeaningCloudParser()
# mcp.load_data(json1)
#
# # "data/meaningCloud_output_json"
#
# f = open(DATA_DIR + 'meaningCloud_output_json/102_winograd.json', 'r')
# mcp2 = MeaningCloudParser()
# mcp2.load_data(f.read())
#
#
# mcp2.do_tests()
# mcp2.test_prop_getter()


# f = open(DATA_DIR + 'meaningCloud_output_json/166_winograd.json', 'r')
# mcp3 = MeaningCloudParser()
# mcp3.load_data(f.read())
# # mcp3.test_prop_getter()
# mcp3.find_swaps()

do_winograd_subs()

# write_dir_subs("")
# json = [{'entity': 'Carlsbad, California', 'ner_type':'LOCATION'},{'entity': 'Dealstruck Inc', 'ner_type':'ORGANIZATION:COMPANY'}]
# test_winograd(print_solution=True)
