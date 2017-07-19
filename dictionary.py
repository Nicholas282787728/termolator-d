import os
from utilspie.collectionsutils import frozendict
from typing import List, Dict
from DataDef import File
import term_utilities

##
#   Dictionaries
#
DICT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + os.sep + "dicts" + os.sep
## DICT_DIRECTORY = '../'
## DICT_DIRECTORY = './'
ORG_DICTIONARY: File = File(DICT_DIRECTORY + 'org_dict.txt')
LOC_DICTIONARY: File = File(DICT_DIRECTORY + 'location-lisp2-ugly.dict')
#
#   @semanticbeeng not used
#
# NAT_DICTIONARY = DICT_DIRECTORY + 'nationalities.dict'
# DISC_DICTIONARY = DICT_DIRECTORY + 'discourse.dict'
# TERM_REL_DICTIONARY = DICT_DIRECTORY + 'term_relation.dict'

nom_file: File = File(DICT_DIRECTORY + 'NOMLIST.dict')
pos_file: File = File(DICT_DIRECTORY + 'POS.dict')
nom_map_file: File = File(DICT_DIRECTORY + 'nom_map.dict')
person_name_file: File = File(DICT_DIRECTORY + 'person_name_list.dict')
nat_name_file: File = File(DICT_DIRECTORY + 'nationalities_name_list.dict')
skippable_adj_file: File = File(DICT_DIRECTORY + 'out_adjectives.dict')
out_ing_file: File = File(DICT_DIRECTORY + 'out_ing.dict')
time_name_file: File = File(DICT_DIRECTORY + 'time_names.dict')
verb_morph_file: File = File(DICT_DIRECTORY + 'verb-morph-2000.dict')
noun_morph_file: File = File(DICT_DIRECTORY + 'noun-morph-2000.dict')

jargon_files: List[File] = [File(DICT_DIRECTORY + 'chemicals.dict'), File(DICT_DIRECTORY + 'more_jargon_words.dict')]

dictionary_table: Dict[str, str] = {'legal': DICT_DIRECTORY + 'legal_dictionary.dict'}
special_domains: List[str] = []

stat_adj_dict: Dict[str, int] = {}  ## @func comp_termChunker, @arch static state
stat_term_dict: Dict[str, bool] = {}  ## @func comp_termChunker, @arch static state
noun_base_form_dict: Dict[str, List[str]] = {}  ## @func comp_termChunker, @arch static state
plural_dict: Dict[str, List[str]] = {}  ## @arch static state
verb_base_form_dict: Dict[str, List[str]] = {}  ## @arch static state
verb_variants_dict: Dict[str, List[str]] = {}  ## @arch static state
nom_dict: Dict[str, str] = {}
pos_dict: Dict[str, List[str]] = {}
jargon_words = set()        # @semanticbeeng @todo @arch global state mutated or read only?

organization_dictionary: Dict[str, Dict[str, str]] = {}     # @semanticbeeng @todo @arch global state mutated or read only?
location_dictionary: Dict[str, Dict[str, str]] = {}
nationality_dictionary: Dict[str, Dict[str, str]] = {}
nom_map_dict: Dict[str, str] = {}
# unigram_dictionary = set()        # @semanticbeeng not used
## add all observed words (in the foreground set) to unigram_dictionary

#
#
#
def add_dictionary_entry(line: str, dictionary: str, shallow: bool, lower: bool=False, patent: bool=False):

    clean_line: str = line.strip(os.linesep + '(\t')

    if clean_line[-1] == ")":
        clean_line = clean_line[:-1]

    clean_line = term_utilities.fix_stray_colons(clean_line)
    line_list: List[str] = clean_line.split(':')

    for index in range(len(line_list)):
        line_list[index] = term_utilities.return_stray_colons(line_list[index])

    # @semanticbeeng not used entry_type = line_list[0].strip(' ')
    entry_dict: Dict[str, str] = {}
    # @semanticbeeng not used current_key = False
    # @semanticbeeng not used current_value = False
    # @semanticbeeng not used started_string = False

    for key_value in line_list[1:]:
        # kv: str = key_value.strip(' ')
        kv = term_utilities.get_key_value(key_value.strip(' '))
        key = kv[0]
        value = kv[1]
        entry_dict[key] = value

    if dictionary == 'org':
        if lower:
            orth = entry_dict['ORTH'].lower()
        else:
            orth = entry_dict['ORTH'].upper()
        organization_dictionary[orth] = entry_dict
    elif dictionary == 'loc':
        if lower:
            orth = entry_dict['ORTH'].lower()
        else:
            orth = entry_dict['ORTH'].upper()
        location_dictionary[orth] = entry_dict
    elif dictionary == 'nat':
        if lower:
            orth = entry_dict['ORTH'].lower()
        else:
            orth = entry_dict['ORTH'].upper()
        nationality_dictionary[orth] = entry_dict
    elif dictionary in ['discourse', 'term_relation']:
        raise Exception('undefined variable discourse_dictionary and term_rel_dictionary')       # @semanticbeeng @todo dead code
        # if dictionary == 'discourse':
        #     actual_dict = discourse_dictionary
        # else:
        #     actual_dict = term_rel_dictionary
        #
        # if shallow and ('SHALLOW_LOW_CONF' in entry_dict):
        #     pass
        # elif ('PATENT_ONLY' in entry_dict) and (not patent):
        #     pass
        # elif ('ARTICLE_ONLY' in entry_dict) and patent:
        #     pass
        # elif 'FORMS' in entry_dict:
        #     forms = entry_dict['FORMS']
        #     entry_dict.pop('FORMS')
        #     word = entry_dict.pop('ORTH')
        #     word = word.lower()
        #     for num in range(len(forms)):
        #         forms[num] = forms[num].lower()
        #     for form in forms:
        #         new_entry = entry_dict.copy()
        #         new_entry['ORTH'] = form
        #         form = form.upper()
        #         if form in actual_dict:
        #             actual_dict[form].append(new_entry)
        #         else:
        #             actual_dict[form] = [new_entry]
        # elif entry_dict['ORTH'].upper() in actual_dict:
        #     actual_dict[entry_dict['ORTH'].upper()].append(entry_dict)
        # else:
        #     actual_dict[entry_dict['ORTH'].upper()] = [entry_dict]


#
#   @semanticbeeng @todo @arch global state initialization
#
def read_in_org_dictionary(dict_file: File, dictionary: str='org', shallow: bool=True, lower: bool=False, patent: bool=False) -> None:

    global organization_dictionary
    global location_dictionary
    global nationality_dictionary

    if dictionary == 'org':
        organization_dictionary.clear()
    elif dictionary == 'loc':
        location_dictionary.clear()
    elif dictionary == 'nat':
        nationality_dictionary.clear()
    elif dictionary == 'discourse':
        raise Exception('undefined variable discourse_dictionary')       # @semanticbeeng @todo dead code
        # discourse_dictionary.clear()
    elif dictionary == 'term_relation':
        raise Exception('undefined variable term_rel_dictionary')       # @semanticbeeng @todo dead code
        # term_rel_dictionary.clear()

    with dict_file.openText(mode='r') as instream:
        for line in instream.readlines():
            add_dictionary_entry(line, dictionary, shallow, lower=lower, patent=patent)

    # @semanticbeeng @arch global state immutable
    if dictionary == 'org':
        organization_dictionary = freeze_dict(organization_dictionary)
    elif dictionary == 'loc':
        location_dictionary = freeze_dict(location_dictionary)
    elif dictionary == 'nat':
        nationality_dictionary = freeze_dict(nationality_dictionary)


#
#
#
def read_in_nom_map_dict() -> None:
    global nom_map_file
    global nom_map_dict

    for line in nom_map_file.openText().readlines():
        word, nominalization = line.strip().split('\t')
        nom_map_dict[word] = nominalization

    # @semanticbeeng @arch global state immutable
    nom_map_dict = freeze_dict(nom_map_dict)


#
#   @semanticbeeng @todo global state initialization
#   @func comp_termChunker
#
def read_in_noun_morph_file() -> None:
    global noun_base_form_dict
    global plural_dict
    global noun_morph_file

    plural_dict.clear()
    noun_base_form_dict.clear()

    for line in noun_morph_file.openText().readlines():
        line_entry: List[str] = line.strip().split('\t')
        word = line_entry[0]
        base = line_entry[1]

        if (word in noun_base_form_dict):
            if not (base in noun_base_form_dict[word]):
                noun_base_form_dict[word].append(base)
        else:
            noun_base_form_dict[word] = [base]

    for word in noun_base_form_dict:
        if not (word in noun_base_form_dict[word]):
            for base_form in noun_base_form_dict[word]:
                if base_form in plural_dict:
                    plural_dict[base_form].append(word)
                else:
                    plural_dict[base_form] = [word]

    # @semanticbeeng @arch global state immutable
    plural_dict = freeze_dict(plural_dict)
    noun_base_form_dict = freeze_dict(noun_base_form_dict)


#
#   @semanticbeeng @todo @arch global state initialization
#
def read_in_verb_morph_file() -> None:
    global verb_morph_file
    global verb_base_form_dict
    global verb_variants_dict

    verb_base_form_dict.clear()
    verb_variants_dict.clear()

    for line in verb_morph_file.openText().readlines():
        line_entry: List[str] = line.strip().split('\t')
        word = line_entry[0]
        base = line_entry[1]

        if (word in verb_base_form_dict):
            verb_base_form_dict[word].append(base)
        else:
            verb_base_form_dict[word] = [base]

    for word in verb_base_form_dict:
        for base_form in verb_base_form_dict[word]:
            if base_form in verb_variants_dict:
                verb_variants_dict[base_form].append(word)
            else:
                verb_variants_dict[base_form] = [word]

    # @semanticbeeng @arch global state immutable
    verb_base_form_dict = freeze_dict(verb_base_form_dict)
    verb_variants_dict = freeze_dict(verb_variants_dict)


#
#
#
def read_in_pos_file() -> None:
    global pos_dict
    global pos_file
    global jargon_files
    pos_dict.clear()

    for line in pos_file.openText().readlines():
        line = line.strip()
        items = line.split('\t')
        pos_dict[items[0]] = items[1:]

    for dictionary in special_domains:
        jargon_files.append(File(dictionary_table[dictionary]))

    for jargon_file in jargon_files:
        ## remove jargon from dictionary
        with jargon_file.openText() as instream:
            for line in instream.readlines():
                word: str = line.strip()
                word = word.lower()
                if word in pos_dict:
                    ## pos_dict.pop(word)
                    jargon_words.add(word)


#
# @semanticbeeng @arch global state immutable
#
def freeze_dict(d: Dict) -> Dict:
    return (frozendict(d))


#
#   Does not "update" but initializes pos_dict
#   @semanticbeeng @todo @arch global state ??
#
def update_pos_dict(name_infiles: List[File]=[person_name_file, nat_name_file],
                    other_infiles: List[File]=[skippable_adj_file, out_ing_file, time_name_file]) -> None:
    global pos_dict

    for infile in name_infiles:
        for line in infile.openText().readlines():
            line = line.strip()
            word, word_class = line.split('\t')
            word = word.lower()
            if word in pos_dict:
                pos_dict[word].append(word_class)
            else:
                pos_dict[word] = [word_class]

    for infile in other_infiles:
        for line in infile.openText().readlines():
            line = line.strip()
            out_list: List[str] = line.split('\t')
            word = out_list[0]
            word_class = out_list[1]

            if len(out_list) > 2:
                flag = out_list[2]
            else:
                flag = None             # @semanticbeeng @todo static typing fix
            word = word.lower()

            if flag == 'ABSOLUTE':
                pos_dict[word] = [word_class]
            elif word in pos_dict:
                pos_dict[word].append(word_class)
            else:
                pos_dict[word] = [word_class]

    for word in term_utilities.patent_stop_words:
        pos_dict[word] = ['OTHER']
        ## treat stop words as inadmissable parts of terms

    for word in term_utilities.NE_stop_words:
        pos_dict[word] = ['OTHER']


#
#
#
def read_in_nom_dict():
    global nom_dict
    global nom_file

    for line in nom_file.openText().readlines():
        nom_class, word = line.strip().split('\t')
        if word in nom_dict:
            nom_dict[word].append(nom_class)
        else:
            nom_dict[word] = [nom_class]

    # @semanticbeeng @arch global state immutable
    nom_dict = freeze_dict(nom_dict)


#
#   @semanticbeeng @todo @arch global state initialization
#   @todo refactor all dictionary stuff into a separate module
#
def initialize_utilities():

    read_in_pos_file()
    update_pos_dict()

    global pos_dict
    # @semanticbeeng @arch global state immutable
    pos_dict = freeze_dict(pos_dict)

    read_in_org_dictionary(ORG_DICTIONARY, dictionary='org', lower=True)
    read_in_org_dictionary(LOC_DICTIONARY, dictionary='loc', lower=True)
    read_in_nom_map_dict()
    read_in_verb_morph_file()
    read_in_noun_morph_file()
    read_in_nom_dict()

    if 'legal' in special_domains:
        term_utilities.parentheses_pattern2 = term_utilities.parentheses_pattern2b
        term_utilities.parentheses_pattern3 = term_utilities.parentheses_pattern3b
    else:
        term_utilities.parentheses_pattern2 = term_utilities.parentheses_pattern2a
        term_utilities.parentheses_pattern3 = term_utilities.parentheses_pattern3a


#
# @semanticbeeng @todo dead code
# @semanticbeeng @arch global state mutation
# @semanticbeeng @func comp_termChunker
#
def read_in_stat_term_dict(indict, dict_dir=DICT_DIRECTORY):
    global stat_term_dict
    global stat_adj_dict

    stat_term_dict.clear()
    stat_adj_dict.clear()

    with open(dict_dir + indict) as instream:
        for line in instream.readlines():
            line_entry = line.strip().split('\t')
            stat_term_dict[line_entry[0]] = True

            if ' ' in line_entry[0]:
                position: int = line_entry[0].index(' ')
                first_word: str = line_entry[0][:position].lower()
            else:
                first_word = line_entry[0].lower()

            pos = guess_pos(first_word, False)

            if pos in ['ADJECTIVE', 'SKIPABLE_ADJ', 'TECH_ADJECTIVE']:
                if not first_word in stat_adj_dict:
                    stat_adj_dict[first_word] = 1
                else:
                    stat_adj_dict[first_word] = stat_adj_dict[first_word] + 1

    adj_threshold = 5  ## not sure what this number should be

    for key in list(stat_adj_dict.keys()):
        if stat_adj_dict[key] < adj_threshold:
            stat_adj_dict.pop(key)

    # @semanticbeeng @arch global state immutable
    stat_term_dict = frozendict(stat_term_dict)
    stat_adj_dict = frozendict(stat_adj_dict)

