import os
# import random
import dictionary
import re
from typing import List, Dict, Tuple, Pattern, Match, Optional
from DataDef import File, POS, TXT3
from refactoring_support import Debug

pos_offset_table: Dict[int, str] = {}

## abbreviate patterns -- the b patterns ignore square brackets
# global parentheses_pattern2
# global parentheses_pattern3
parentheses_pattern2a: Pattern[str] = re.compile(r'[(\[]([ \t]*)([^)\]]*)([)\]]|$)')
parentheses_pattern3a: Pattern[str] = re.compile(r'(\s|^)[(\[]([^)\]]*)([)\]]|$)([^a-zA-Z0-9-]|$)')
parentheses_pattern2b: Pattern[str] = re.compile(r'[(]([ \t]*)([^)]*)([)]|$)')
parentheses_pattern3b: Pattern[str] = re.compile(r'(\s|^)[(]([^)]*)([)\]]|$)([^a-zA-Z0-9-]|$)')


closed_class_stop_words: List[str] = \
    ['a', 'the', 'an', 'and', 'or', 'but', 'about', 'above', 'after', 'along', 'amid', 'among',
     'as', 'at', 'by', 'for', 'from', 'in', 'into', 'like', 'minus', 'near', 'of', 'off', 'on',
     'onto', 'out', 'over', 'past', 'per', 'plus', 'since', 'till', 'to', 'under', 'until', 'up',
     'via', 'vs', 'with', 'that', 'can', 'cannot', 'could', 'may', 'might', 'must',
     'need', 'ought', 'shall', 'should', 'will', 'would', 'have', 'had', 'has', 'having', 'be',
     'is', 'am', 'are', 'was', 'were', 'being', 'been', 'get', 'gets', 'got', 'gotten',
     'getting', 'seem', 'seeming', 'seems', 'seemed',
     'enough', 'both', 'all', 'your' 'those', 'this', 'these',
     'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',
     'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',
     'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',
     'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',
     'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',
     'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',
     'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',
     'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace',
     'anything', 'anytime' 'anywhere', 'everybody', 'everyday',
     'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',
     'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',
     'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their', 'theirs',
     'you', 'your', 'yours', 'me', 'my', 'mine', 'I', 'we', 'us', 'much', 'and/or'
     ]
## ABBREVIATION_STOP_WORDS plus some

patent_stop_words: List[str] = \
    ['patent', 'provisional', 'kokai', 'open', 'publication', 'number', 'nos', 'serial',
     'related', 'claim', 'claims', 'embodiment', 'related', 'present', 'priority', 'design',
     'said', 'respective', 'fig', 'figs', 'copyright', 'following', 'preceding', 'according',
     'barring', 'pending', 'pertaining', 'international', 'wo', 'pct']

signal_set: List[str] = \
    ['academically', 'accordance', 'according', 'accordingly', 'actuality', 'actually', 'addition', 'additionally', 'administratively', 'admittedly', 'aesthetically',
     'agreement', 'alarmingly', 'alas', 'all', 'allegedly', 'also', 'alternative', 'alternatively', 'although', 'altogether', 'amazingly', 'analogously', 'anyhow',
     'anyway', 'anyways', 'apparently', 'appropriately', 'architecturally', 'arguably', 'arithmetically', 'artistically', 'as', 'assumingly', 'assuredly', 'astonishingly',
     'astronomically', 'asymptotically', 'atypically', 'axiomatically', 'base', 'based', 'bases', 'basing', 'besides', 'biologically', 'but', 'case', 'certainly',
     'coincidentally', 'colloquially', 'combination', 'combine', 'combined', 'combines', 'combining', 'commercially', 'compared', 'comparison', 'compliance',
     'computationally', 'conceivably', 'conceptually', 'concord', 'concordance', 'confirm', 'confirmation', 'confirmed', 'confirming', 'confirms', 'conformity',
     'consequence', 'consequentially', 'consequently', 'consistent', 'constitutionally', 'constrasts', 'contrarily', 'contrariwise', 'contrary', 'contrast', 'contrasted',
     'contrasting', 'contrastingly', 'controversially', 'conversely', 'correlate', 'correlated', 'correlates', 'correlation', 'correspondingly', 'corroborate',
     'corroborated', 'corroborates', 'corroborating', 'corroboration', 'couple', 'coupled', 'couples', 'coupling', 'course', 'curiously', 'definitely', 'described',
     'descriptively', 'despite', 'done', 'doubtless', 'doubtlessly', 'due', 'ecologically', 'economically', 'effect', 'effectively', 'else', 'empirically', 'endorse',
     'endorsed', 'endorsement', 'endorses', 'environmentally', 'ethically', 'event', 'eventually', 'evidently', 'example', 'excitingly', 'extend', 'extended', 'extending',
     'extends', 'extension', 'fact', 'factually', 'far', 'fifthly', 'finally', 'first', 'firstly', 'following', 'formally', 'fortunately', 'fourth', 'fourthly', 'frankly',
     'further', 'furthermore', 'genealogically', 'general', 'generally', 'genetically', 'geographically', 'geologically', 'geometrically', 'grammatically', 'gratuitously',
     'hand', 'hence', 'historically', 'honestly', 'honesty', 'hopefully', 'however', 'ideally', 'implement', 'implementation', 'implemented', 'implementing', 'implements',
     'incidentally', 'increasingly', 'indeed', 'indubitably', 'inevitably', 'informally', 'instance', 'instead', 'institutionally', 'interestingly', 'intriguingly',
     'invoke', 'invoked', 'invokes', 'invoking', 'ironically', 'journalistically', 'lamentably', 'last', 'lastly', 'legally', 'lest', 'light', 'likelihood', 'likewise',
     'line', 'linguistically', 'literally', 'logically', 'luckily', 'lyrically', 'manner', 'materialistically', 'mathematically', 'meantime', 'meanwhile', 'mechanically',
     'mechanistically', 'medically', 'melodramatically', 'merge', 'merged', 'merges', 'merging', 'metaphorically', 'metaphysically', 'methodologically', 'metrically',
     'militarily', 'ministerially', 'miraculously', 'mix', 'mixed', 'mixes', 'mixing', 'mixture', 'modestly', 'morally', 'moreover', 'morphologically', 'mundanely',
     'musically', 'mutandis', 'mutatis', 'naturally', 'nay', 'necessarily', 'needfully', 'nevertheless', 'next', 'nonetheless', 'normally', 'not', 'notwithstanding',
     'now', 'numerically', 'nutritionally', 'objectionably', 'obscenely', 'observably', 'obviously', 'oddly', 'odds-on', 'of', 'offhand', 'officially', 'ominously',
     'optimally', 'optimistically', 'ordinarily', 'originally', 'ostensibly', 'otherwise', 'overall', 'paradoxically', 'parenthetically', 'particular', 'peculiarly',
     'perceptively', 'perchance', 'personally', 'perversely', 'pessimistically', 'pettily', 'pharmacologically', 'philanthropically', 'philosophically', 'phonetically',
     'photographically', 'physically', 'plausibly', 'poetically', 'politically', 'possibly', 'potentially', 'practically', 'pragmatically', 'predictably', 'preferably',
     'presumably', 'presumptively', 'probabilistically', 'probability', 'probably', 'problematically', 'professedly', 'propitiously', 'rashly', 'rate', 'rather',
     'rationally', 'realistically', 'really', 'reference', 'regardless', 'regretfully', 'regrettably', 'reportedly', 'reputedly', 'result', 'retrospectively',
     'rhetorically', 'ridiculously', 'roughly', 'sceptically', 'scientifically', 'second', 'secondly', 'separately', 'seriously', 'shockingly', 'similar', 'similarly',
     'simultaneously', 'somehow', 'speaking', 'specifically', 'statistically', 'still', 'strangely', 'strikingly', 'subsequently', 'superficially', 'superstitiously',
     'support', 'supported', 'supporting', 'supports', 'supposedly', 'surely', 'surprisingly', 'symbolically', 'tactically', 'take', 'taken', 'takes', 'taking',
     'technically', 'thankfully', 'thanks', 'then', 'thence', 'theologically', 'theoretically', 'thereafter', 'therefore', 'third', 'thirdly', 'though', 'thus', 'time',
     'took', 'touchingly', 'traditionally', 'tragically', 'trivially', 'truly', 'truth', 'truthfully', 'ultimately', 'unaccountably', 'unarguably', 'undeniably',
     'understandably', 'undisputedly', 'undoubtedly', 'unexpectedly', 'unfortunately', 'unsurprisingly', 'use', 'used', 'uses', 'using', 'usually', 'utilization',
     'utilize', 'utilized', 'utilizes', 'utilizing', 'verily', 'view', 'way', 'whence', 'whereas', 'whereby', 'wherefore', 'wherein', 'whereof', 'whereon', 'whereto',
     'whereunto', 'whereupon', 'while', 'withal', 'worryingly', 'yet']

## ne_stop_words = ['et', 'co', 'al', 'eds','corp','inc','sa','cia','ltd','GmbH','Esq','PhD']

NE_stop_words: List[str] = ['eds', 'publications?', 'et', 'co', 'al', 'eds', 'corp', 'inc', 'sa', 'cia', 'ltd', 'gmbh', 'esq', 'phd', 'natl', 'acad', 'sci', 'proc', 'chem', 'soc']

attribute_value_from_fact: Pattern[str] = re.compile(r'([A-Z0-9_]+) *[=] *((["][^"]*["])|([0-9]+))', re.I)

person_ending_pattern: Pattern[str] = re.compile(' (Esq|PhD|Jr|snr)\.?$', re.I)

org_ending_pattern: Pattern[str] = re.compile(' (corp|inc|sa|cia|ltd|gmbh|co)\.?$', re.I)

closed_class_words2 = r'and|or|as|the|a|of|for|at|on|in|by|into|onto|to|per|plus|through|till|towards?|under|until|via|with|within|without|no|any|each|that|there|et|al'
closed_class_check2: Pattern[str] = re.compile('^(' + closed_class_words2 + ')$', re.I)

organization_word_pattern: Pattern[str] = re.compile(
    r'^(AGENC(Y|IE)|ASSOCIATION|BUREAU|CENT(ER|RE|RO)|COLL[EÈ]GE|COMMISSION|CORP[\.]|CORPORATION|COUNCIL|DEPARTMENT|ENDOWMENT|FOUNDATION|FUND|GROUP|HOSPITAL|(INC|SA|CIA|LTD|CORP|GMBH|CO)\.?|IN?STITUT[EO]?|LABORATOR((Y)|IE)|OFFICE|ORGANI[SZ]ATION|PARTNER|PROGRAMME|PROGRAM|PROJECT|SCHOOL|SOCIET(Y|IE)|TRUST|(UNIVERSI[TD](AD)?(E|É|Y|IE|À|ÄT)?)|UNIVERSITÄTSKLINIKUM|UNIVERSITÄTSSPITAL)S?$',
    re.I)

last_word_organization: Pattern[str] = re.compile(
    r'^(AGENC(Y|IE)|ASSOCIATION|CENT(ER|RE|RO)|COLL[EÈ]GE|COMMISSION|CORP[\.]|CORPORATION|COUNCIL|DEPARTMENT|ENDOWMENT|FOUNDATION|FUND|GROUP|HOSPITAL|(INC|SA|CIA|LTD|CORP|GMBH|CO)\.?|IN?STITUT[EO]?|LABORATOR((Y)|IE)|OFFICE|ORGANI[SZ]ATION|PARTNER|PROGRAMME|PROGRAM|PROJECT|SCHOOL|SOCIET(Y|IE)|TRUST|(UNIVERSI[TD](AD)?(E|É|Y|IE|À|ÄT)?)|UNIVERSITÄTSKLINIKUM|UNIVERSITÄTSSPITAL|INDUSTRIE|PRESS|SOLUTIONS|TELECOMMUNICATIONS|TECHNOLOGIE|PHARMACEUTICAL|CHEMICAL|BIOSCIENCE|BIOSYSTEM|BIOTECHNOLOG(Y|IE)|INSTRUMENT|SYSTEMS|COMPANY|INST|RES|ABSTRACTS|ASSOC(ITATES)?|SCIENTIFICA|UNION)S?$',
    re.I)

ambig_last_word_org: Pattern[str] = re.compile(r'^(PROGRAM|SYSTEM)S?$', re.I)

last_word_gpe: Pattern[str] = re.compile(r'(HEIGHTS?|MASS|TOWNSHIP|PARK)$', re.I)

last_word_loc: Pattern[str] = re.compile(r'(STREET|AVENUE|BOULEVARD|LANE|PLACE)$', re.I)

xml_pattern: Pattern[str] = re.compile(r'<([/!?]?)([a-z?\-]+)[^>]*>', re.I)

xml_string: str = '<([/!?]?)([a-z?\-]+)[^>]*>'


html_fields_to_remove = ['style', 'script']

text_html_fields = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'dt', 'dd', 'address', 'pre', 'td', 'caption', 'br']
## some of these may require additional formatting to properly process them, e.g.,
## the following (not implemented) may require additional new lines: address, pre

roman_value: Dict[str, int] = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}


def ok_roman_bigram(pair: str) -> bool:
    if pair in ['ii', 'iv', 'ix', 'vi', 'xi', 'xv', 'xx', 'xl', 'xc', 'li', 'lv', 'lx', 'ci', 'cv', 'cx', 'cl', 'cc', 'cd', 'cm', 'mi', 'mv', 'mx', 'ml', 'mc', 'md', 'mm']:
        return (True)
    else:
        return (False)


def OK_roman_trigram(triple: str) -> bool:
    if triple in ['ivi', 'ixi', 'xlx', 'xcx', 'cdc', 'cmc']:
        return (False)
    else:
        return (True)


def roman(string: str) -> bool:
    lower = string.lower()
    if (type(lower) == str) and re.search('^[ivxlcdm]+$', lower):
        ## lower consists completely of correct characters (unigram)
        ## now check bigrams
        result = True
        for position in range(len(lower)):
            if ((position == 0) or ok_roman_bigram(lower[position - 1:position + 1])) and \
                    ((position < 2) or OK_roman_trigram(lower[position - 2:position + 1])):
                pass
            else:
                result = False
        return (result)
    else:
        return (False)


def evaluate_roman(string: str) -> int:
    total = 0
    value_list: List[int] = []
    for character in string:
        value_list.append(roman_value[character.lower()])
    last: int = value_list[0]

    for number in value_list[1:]:
        if last and (last < number):
            total = total + (number - last)
            last = False
        elif last and (last >= number):
            total = total + last
            last = number
        else:
            last = number
    if last != 100000000:
        total = total + last
    return (total)


def return_stray_colons(string: str) -> str:
    return (string.replace('-colon-', ':'))


def fix_stray_colons(string: str) -> str:
    position = string.find(':')
    if position == -1:
        output = string
    elif position == 0 or string[position + 1] != ' ':
        border = 1 + position
        output = string[:border] + fix_stray_colons(string[border:])
    else:
        border = 1 + position
        output = string[:position] + '-colon-' + fix_stray_colons(string[border:])
    return (output)


# #
# #   @semanticbeeng dead code
# #
# def is_lisp_key_word(string):
#     return (string[0] == ':')


def list_starter(string: str) -> bool:
    return (string[0] == '(')


def list_ender(string: str) -> bool:
    return (string[-1] == ')')


def string_starter(string: str) -> bool:
    return (string[0] == '"')


def string_ender(string: str) -> bool:
    return (string[-1] == '"')


#
#
#
def process_lexicon_list(value: str) -> List[str]:
    output = []
    value = value.strip('()')
    if '"' in value:
        value_list = value.split('"')
    else:
        value_list = value.split(' ')

    if "" in value_list:
        value_list.remove('')

    for item in value_list:
        item = item.strip(' ')
        if item != '':
            output.append(item)
    return (output)


#
#   @semanticbeeng @todo static type - conflict between List and Tuple; maybe to a conversion?
#
def get_key_value(string: str) -> Tuple[str, List[str]]:

    initial_list: Tuple[str, str, str] = string.partition(' ')
    key: str = initial_list[0]
    value: str = initial_list[2].strip(' ')
    value_list: List[str] = [value]

    if list_starter(value):
        if list_ender(value):
            value_list = process_lexicon_list(value)
        else:
            print('string', string)
            print('value', value)
            raise Exception('Current Program cannot handle recursive structures')

    elif string_starter(value) and string_ender(value):
        value = value.strip('"')
        value_list = [value]

    return (key, value_list)         # @semanticbeeng @todo verify okay to return List @done


#
#
#
def parentheses_pattern_match(instring: str, start: int, pattern_number: int) -> Optional[Match[str]]:
    if 'legal' in dictionary.special_domains:
        if pattern_number == 2:
            return (parentheses_pattern2b.search(instring, start))
        else:
            return (parentheses_pattern3b.search(instring, start))
    else:
        if pattern_number == 2:
            return (parentheses_pattern2a.search(instring, start))
        else:
            return (parentheses_pattern3a.search(instring, start))


def breakup_line_into_chunks(inline: str, difference: int) -> List[str]:
    size = 1000
    start = 0
    if difference == 0:
        ## this seems to happen sometimes
        ## perhaps this is the case where
        ## the current filters do not
        ## detect good break points
        return ([inline])
    output = []
    while start < len(inline):
        end = start + size
        if end >= len(inline):
            output.append(inline[start:])
        else:
            output.append(inline[start:end - difference])
            start = end
    return (output)


def table_upper_split(line: str) -> List[str]:
    ## in order to maintain offsets this program will delete
    ## one non-alphanumeric character or upper case character
    ## per new line created
    ## since other programs assume a newline character between
    ## lines.
    difference: int = 0
    table_pattern: Pattern[str] = re.compile('[^a-zA-Z0-9]TABLE[^a-zA-Z0-9]')
    end_table_pattern: Pattern[str] = re.compile('[A-Za-z][a-z]')
    table_start: Optional[Match[str]] = table_pattern.search(line)
    output: List[str] = []
    start: int = 0

    if not table_start:
        return ([line])

    while table_start:
        output.append(line[start:table_start.start() - difference])
        end_table: Optional[Match[str]] = end_table_pattern.search(line, table_start.end())

        if end_table:
            output.append(line[table_start.start() + difference:end_table.start()])
            start = end_table.start()
            table_start = table_pattern.search(line, start)
        else:
            output.append(line[start:])
            start = len(line)
            table_start = None      # @semanticbeeng static typing

    output2: List[str] = []

    if start < len(line):
        output.append(line[start:])

    for out in output:
        if len(out) < 3000:
            output2.append(out)
        else:
            output2.extend(breakup_line_into_chunks(out, difference))
    return (output2)


def long_line_split(input_line: str):
    ## really long lines can be problematic
    ## one case we found is inserted tables
    ## we will start with these.
    ## if we find more cases, this
    ## function can increase in complexity
    if len(input_line) < 2000:
        return ([input_line])
    else:
        return (table_upper_split(input_line))


def remove_xml(string: str) -> str:
    output = xml_pattern.sub('', string)
    return (output)


#
#
#
def clean_string_of_ampersand_characters(string: str) -> str:
    ampersand_char_pattern = re.compile('&[^;]+;')
    ampersand_char_pattern2 = re.compile('&[^;<]+[<]')
    match = ampersand_char_pattern.search(string)

    if not match:
        match = ampersand_char_pattern2.search(string)

    while match:
        if match.group(0).endswith('<'):
            string = string[:match.start()] + (len(match.group(0)) - 1) * ' ' + string[match.end() - 1:]
        else:
            string = string[:match.start()] + len(match.group(0)) * ' ' + string[match.end():]
        match = ampersand_char_pattern.search(string)
        if not match:
            match = ampersand_char_pattern2.search(string)
    return (string)


#
#
#
def remove_xml_spit_out_paragraph_start_end(string: str, offset) -> Tuple[str, List[int], List[int], List[int], List[int]]:
    string = clean_string_of_ampersand_characters(string)
    next_xml = xml_pattern.search(string)
    start = 0
    out_string = ''
    # bare_string_border = 0
    paragraph_starts: List[int] = []
    paragraph_ends: List[int] = []
    remove_starts: List[int] = []
    remove_ends: List[int] = []

    while next_xml:
        out_string = out_string + string[start:next_xml.start()]

        if next_xml.group(2).lower() in text_html_fields:
            if next_xml.group(1) == '/':
                paragraph_ends.append(len(out_string) + offset)
            else:
                paragraph_starts.append(len(out_string) + offset)
        elif next_xml.group(2).lower() in html_fields_to_remove:
            if next_xml.group(1) == '/':
                remove_ends.append(len(out_string) + offset)
            else:
                remove_starts.append(len(out_string) + offset)

        start = next_xml.end()
        next_xml = xml_pattern.search(string, start)

    out_string = out_string + string[start:]

    return (out_string, paragraph_starts, paragraph_ends, remove_starts, remove_ends)


#
#
#
def replace_less_than_with_positions(string: str, offset: int) -> Tuple[str, List[List[int]]]:
    out_string = ''
    num = 0
    less_thans: List[List[int]] = []
    length = len(string)

    for char in string:
        if char == '<':
            start = num + offset
            if (num < (length - 1)) and (string[num + 1] == ' '):
                plus = 2
            else:
                plus = 1
            less_thans.append([num + offset, num + offset + plus])
            out_string = out_string + ' '
        else:
            out_string = out_string + char
        num = num + 1
    return (out_string, less_thans)


#
#
#
def interior_white_space_trim(instring: str) -> str:
    out1 = re.sub('\s+', ' ', instring)
    out2 = re.sub('\s*(.*[^\s])\s*$', '\g<1>', out1)
    return (out2)


#
#
#
def isStub(line: str) -> bool:
    if (len(line) < 1000) and re.search('[\(\[][ \t]*$', line):
        return (True)
    return (False)

#
# @semanticbeeng static typing : TXT3 contains paragraphs (str)
#
def get_lines_from_file(infile: File[TXT3]) -> List[str]:

    # @semanticbeeng @todo @jep
    # with infile.openText(mode='r') as instream:
    instream = infile.openText('r')
    output: List[str] = []
    short_line: Optional[str] = None        # @semanticbeeng @todo static type

    for line in instream.readlines():
        line = remove_xml(line)
        if short_line:
            line = short_line + line
        if isStub(line):
            short_line = re.sub(os.linesep, ' ', line)
        else:
            short_line = None
            for line2 in long_line_split(line):
                output.append(line2)
    if short_line:
        output.append(short_line)
    return (output)


#
#   @semanticbeeng @todo consider moving this to dictionary.py
#   @semanticbeeng @todo global state mutation or initialization ?
#
def load_pos_offset_table(pos_file: File[POS]) -> None:
    global pos_offset_table
    pos_offset_table.clear()

    if os.path.isfile(pos_file.name):
        # @semanticbeeng @todo @jep
        # with pos_file.openText() as instream:
        instream = pos_file.openText()
        for line in instream.readlines():
            line_info: List[str] = line.rstrip().split(' ||| ')
            start_end = line_info[1]
            start_end_strings = start_end.split(' ')
            start = int(start_end_strings[0][2:])
            pos = line_info[2]
            pos_offset_table[start] = pos


#
#
#
def citation_number(word: str) -> bool:
    ## There may still be clashes with standard
    patent_number = r'((A-Z)*([0-9,/-]{4,})(A-Z)*)|([0-9][0-9]+( [0-9][0-9]+)+((([.-][0-9]+)| [A-Z][0-9]+)?)+)|([0-9][0-9]/[0-9]{3},[0-9]{3})|(PCT/[A-Z]{2}[0-9]{2,4}/[0-9]{5,})'
    german_patent = r'DE(-OS)? [0-9][0-9]+( [0-9][0-9]+)+(([.][0-9]+)| [A-Z][0-9]+)?'
    pct_patent = r'(PCT/[A-Z]{2}[0-9]{,4}/[0-9]{5,})'
    isbn = r'ISBN[:]? *([0-9][ -][0-9]{3}[ -][0-9]{2}[ -][0-9]{3}[ -][0-9X])'
    ## these focus on citation IDs that are number+letter combos
    citation_number_match = re.compile('((((U[.]?S[.]?)? *)?(' + patent_number + '))|(' + german_patent + ')|(' + pct_patent + ')|(' + isbn + '))')

    if citation_number_match.search(word):
        return (True)
    else:
        return (False)


#
#
#
def resolve_differences_with_pos_tagger(word: str, offset: Optional[int], dict_pos: List[str], tagger_pos: Optional[str]) -> List[str]:
    if (tagger_pos == 'ADJECTIVE') and ('ORDINAL' in dict_pos):
        return (['ORDINAL'])
    elif (tagger_pos == 'ADJECTIVE') and ('SKIPABLE_ADJ' in dict_pos):
        return (['SKIPABLE_ADJ'])
    elif (tagger_pos == 'ADJECTIVE') and ('NATIONALITY' in dict_pos):
        return (['NATIONALITY_ADJ'])
    elif (tagger_pos in ['ADJECTIVE', 'NOUN']) and \
            (word.endswith('ing') or word.endswith('ed')):
        return ([tagger_pos])
    elif (tagger_pos == 'VERB') and dict_pos and (not 'VERB' in dict_pos):
        return (dict_pos)
    elif tagger_pos in dict_pos:
        return ([tagger_pos])
    elif (tagger_pos == 'OTHER'):
        if ('AUX' in dict_pos) or ('WORD' in dict_pos) or \
                ('CCONJ' in dict_pos) or ('PRONOUN' in dict_pos) or \
                ('TITLE' in dict_pos) or ('SCONJ' in dict_pos) or \
                ('ADVERB' in dict_pos):
            return (['WORD'])
        else:
            return (dict_pos)
    elif ('NATIONALITY' in dict_pos) and (tagger_pos == 'NOUN'):
        return (['NOUN'])       # @semanticbeeng @todo static type: can return List ???
    elif (tagger_pos == 'NOUN') and ('NOUN_OOV' in dict_pos):
        return (['NOUN_OOV'])
    else:
        return (dict_pos)


#
# @func comp_termChunker
#
def closed_class_conflict(word: str) -> bool:
    if word in closed_class_stop_words:
        return (True)
    elif (word in dictionary.noun_base_form_dict):
        for base in (dictionary.noun_base_form_dict[word]):
            if base in closed_class_stop_words:
                return (True)
    return (False)          # @semanticbeeng @todo static typing

#
#
#
def technical_adj(word: str) -> Optional[Match[str]]:
    technical_pattern = re.compile('(ic|[c-x]al|ous|[ao]ry|[coup]id|lar|ine|ian|rse|iac|ive)$')
    ## matches adjectives with certain endings
    return (technical_pattern.search(word))


#
#
#
def id_number_profile(word: str) -> bool:
    digits = len(re.sub('[^0-9]', '', word))
    alpha = len(re.sub('[0-9]', '', word))
    if (digits > 0) and (alpha > 0):
        return (True)
    return (False)          # @semanticbeeng @todo static typing


#
#
#
def verbal_profile(word: str) -> bool:
    if (len(word) > 5) and re.search('[aeiou][b-df-hj-np-ts-z]ed$', word):
        return (True)
    return (False)          # @semanticbeeng @todo static typing


#
#
#
def nom_class(word: str, pos: str) -> int:
    if word in ['invention', 'inventions']:
        return (0)
    ## invention (patents) is usually a self-citation and we want to
    ## downgrade its score
    elif word in dictionary.nom_dict:
        rank = 0
        for feature in dictionary.nom_dict[word]:
            if feature in ['NOM', 'NOMLIKE', 'ABLE-NOM']:
                ## 'NOMADJ', 'NOMADJLIKE'
                ## secondary: ability, attribute, type, group
                ## question NOMADJ and NOMADJLIKE
                if rank < 2:
                    rank = 2
            elif feature in ['ABILITY', 'ATTRIBUTE', 'TYPE', 'GROUP']:
                if rank < 1:
                    rank = 1
        return (rank)  ## return highest possible rank
    elif (pos in ['VERB', 'AMBIG_VERB']) and (len(word) > 5) and (word[-3:] == 'ing'):
        return (1)
    else:
        return (0)


#
#
#
def term_dict_check(term: str, test_dict: Dict[str, int]) -> bool:
    if term in test_dict:
        return (True)
    elif ('-' in term):
        pat = re.search('-([^-]+)$', term)
        if pat and pat.group(1) in test_dict:
            return (True)
    return (False)          # @semanticbeeng @todo static typing


#
# @semanticbeeng func comp_termChunker
# @semanticbeeng global to object @todo
#
def guess_pos(word: str, is_capital: bool, offset: int = None) -> str:  # @semanticbeeng static type @todo
    pos: List[str] = []
    plural = False

    if Debug.run_filter_phase:
        assert not pos_offset_table
        tagger_pos: str = None
    else:
        tagger_pos = get_tagger_pos(offset)

    if (len(word) > 2) and word[-2:] in ['\'s', 's\'']:
        possessive = True
        word = word[:-2]
    else:
        possessive = False

    if (len(word) == 1) and not word.isalnum():
        return ('OTHER')

    if word in dictionary.pos_dict:
        pos = dictionary.pos_dict[word][:]
        if not possessive:
            pos = resolve_differences_with_pos_tagger(word, offset, pos, tagger_pos)
        if ('PERSON_NAME' in pos) and (not is_capital):
            pos.remove('PERSON_NAME')
            if len(pos) == 0:
                pos.append('NOUN_OOV')
        ## initially set pos based on dictionary
        if (word in dictionary.nom_dict) and ('NOM' in dictionary.nom_dict[word]):
            is_nom = True
        else:
            is_nom = False
        if (len(pos) > 1):
            if 'PREP' in pos:
                return ('PREP')
            elif ('DET' in pos) or ('QUANT' in pos) or ('CARDINAL' in pos):
                return ('DET')
            elif ('ADVERB' in pos) and not is_nom:
                return ('ADVERB')
            elif ('AUX' in pos) or ('WORD' in pos) or \
                    ('CCONJ' in pos) or ('PRONOUN' in pos) or \
                    ('TITLE' in pos) or ('SCONJ' in pos):
                return ('OTHER')
            elif (('SKIPABLE_ADJ' in pos) or ('ORDINAL' in pos)) and (not term_dict_check(word.lower(), dictionary.stat_adj_dict)):
                return ('SKIPABLE_ADJ')
            elif (('NOUN' in pos) or ('NOUN_OOV' in pos)) and not closed_class_conflict(word):
                if possessive:
                    return ('AMBIG_POSSESS')
                elif (len(word) > 1) and (word[-1] == 's') and (word in dictionary.noun_base_form_dict) and (not (word in dictionary.noun_base_form_dict[word])):
                    return ('AMBIG_PLURAL')
                else:
                    return ('AMBIG_NOUN')
            elif 'VERB' in pos:
                return ('AMBIG_VERB')
            elif 'ADJECTIVE' in pos:
                if technical_adj(word):
                    return ('TECH_ADJECTIVE')
                else:
                    return ('ADJECTIVE')
            else:
                return ('OTHER')
        elif len(pos) == 1:
            if (('NOUN' in pos) or ('NOUN_OOV' in pos)):
                if possessive:
                    return ('POSSESS')
                elif (len(word) > 1) and (word[-1] == 's') and (word in dictionary.noun_base_form_dict) and (not (word in dictionary.noun_base_form_dict[word])):
                    return ('PLURAL')
                ## plurals are nouns ending in 's' and that are not base forms
                elif 'NOUN_OOV' in pos:
                    return ('NOUN_OOV')
                else:
                    return ('NOUN')
            elif ('PERSON_NAME' in pos):
                if possessive:
                    return ('POSSESS')
                else:
                    return ('PERSON_NAME')
            elif 'VERB' in pos:
                return ('VERB')
            elif 'DET' in pos:
                return ('DET')
            elif 'PREP' in pos:
                return ('PREP')
            elif (('SKIPABLE_ADJ' in pos) or ('ORDINAL' in pos)) and not (term_dict_check(word.lower(), dictionary.stat_adj_dict)):
                return ('SKIPABLE_ADJ')
            elif 'ADJECTIVE' in pos:
                if technical_adj(word):
                    return ('TECH_ADJECTIVE')
                else:
                    return ('ADJECTIVE')
            elif 'PERSON_NAME' in pos:
                return ('PERSON_NAME')
            else:
                return ('OTHER')

    elif (not possessive) and ('-' in word) and re.search('[a-zA-Z]', word):
        little_words = word.split('-')

        if len(little_words) > 2:
            for word in little_words:
                little_pos = guess_pos(word, word.istitle())
                if little_pos == 'NOUN_OOV':
                    return ('NOUN_OOV')
            return ('NOUN')

        if len(little_words) == 1 and (little_words[0].isalnum()):
            return (guess_pos(little_words[0], is_capital))     # @semanticbeeng todo !!
            # return (guess_pos(little_words[0]), is_capital)

        if little_words[1] in dictionary.pos_dict:  ## the last word
            last_pos = dictionary.pos_dict[little_words[1]][:]
            first_pos = guess_pos(little_words[0], little_words[0].istitle())
            first_word = little_words[0].lower()
            if first_pos == 'NOUN_OOV':
                return ('NOUN_OOV')
            if 'ADVPART' in last_pos:
                return ('SKIPABLE_ADJ')
            if 'NOUN' in last_pos:
                if (len(word) > 2) and (word[-1] == 's') and (not word[-2] in "aiousc"):
                    return ('PLURAL')
                elif word[0].isnumeric():
                    return ('ADJECTIVE')
                    ## treat like adjective, like PTB, also to rule out
                else:
                    return ('NOUN')
            elif 'PERSON_NAME' in last_pos:
                return ('NOUN')
            elif 'SKIPABLE_ADJ' in pos:
                if term_dict_check(word.lower(), dictionary.stat_adj_dict):
                    if technical_adj(word):
                        return ('TECH_ADJECTIVE')
                    else:
                        return ('ADJECTIVE')
                else:
                    return ('SKIPABLE_ADJ')
            elif 'ADJECTIVE' in last_pos:
                if technical_adj(word):
                    return ('TECH_ADJECTIVE')
                elif (first_pos == 'NOUN') and ((not first_word in dictionary.pos_dict) or (nom_class(first_word, first_pos) > 1)):
                    return ('TECH_ADJECTIVE')
                else:
                    return ('ADJECTIVE')
            elif 'VERB' in last_pos:
                if word.endswith('ed') or word.endswith('ing'):
                    if (first_pos == 'NOUN') and ((not first_word in dictionary.pos_dict) or (nom_class(first_word, first_pos) > 1)):
                        return ('TECH_ADJECTIVE')
                    else:
                        return ('ADJECTIVE')
                elif 'NOUN' in last_pos:
                    return ('NOUN')
                else:
                    return ('ADJECTIVE')
            else:
                return ('OTHER')
        elif (len(word) > 2) and (word[-1] == 's') and (not word[-2] in "aiousc"):
            return ('PLURAL')
        else:
            return ('NOUN')
    elif (tagger_pos == 'POS') or ((not tagger_pos) and (word in ["'s", "'S"])):
        ## if there is no POS tagger, do not try to find verb cases of "'s"
        return ('POS')
    elif tagger_pos in ['ADVERB', 'VERB']:
        return (tagger_pos)
    elif (tagger_pos in ['ADJECTIVE']):
        ### added at the same time as adding jargon terms
        return ('TECH_ADJECTIVE')
    elif (len(word) > 4) and (word[-2:] == 'ly'):
        ## length requirement will get rid of most enumerations in parens
        return ('ADVERB')
    elif possessive and re.search('^[0-9]+$', word[:-2]):
        ## possessive number
        return ('OTHER')
    elif possessive:
        return ('POSSESS_OOV')
    elif (id_number_profile(word)):
        if citation_number(word):
            return ('OTHER')
        else:
            return ('NOUN_OOV')
    elif re.search('^[0-9\-.\/]+$', word):
        ## here an id_number is any combination of numbers and letters
        ## this may need to be modified to differentiate patent numbers from chemical/virus/etc. names
        ## the second term describes a number consisting of a combination of digits, periods and fractional slashes
        return ('OTHER')
    elif verbal_profile(word):
        ## return('VERB')
        ## long word ending in 'ed'
        return ('TECHNICAL_ADJECTIVE')
    elif (len(word) > 2) and (word[-1] == 's') and (not word[-2] in "aiousc"):
        return ('PLURAL')
        ## assume out-of-vocabulary (OOV) words ending in 's' can be nouns, given the right circumstances
    elif roman(word):
        return ('ROMAN_NUMBER')
    else:
        return ('NOUN_OOV')
        ## otherwise assume most OOV words are nouns
    raise Exception('Unexpected to get here')       # @semanticbeeng


#
#   @ssemanticbeeng @todo @global state pos_offset_table - clarify meaning since it may be empty if raaan from filter_term_output.py
#
def get_tagger_pos(offset: int) -> str:

    if offset and (offset in pos_offset_table):
        tagger_pos = pos_offset_table[offset]  # @semanticbeeng @todo global state reference
        ## Most conservative move is to use for disambiguation,
        ## and for identifying ing nouns (whether NNP or NN)
        ## We care about:
        ## Easy translations: NN NNP NNPS NNS; JJ JJR JJS; RB RBR RBS RP WRB;
        ## 'FW' 'SYM' '-LRB-''-RRB-'; VBD VBG VBN VBP VBZ VB; DT PDT WDT PRP$ WP$
        ## CC CD EX FW LS MD POS PRP UH WP
        if tagger_pos in ['NNP', 'NNPS', 'FW', 'SYM', '-LRB-', '-RRB-']:
            ## these are inaccurate for this corpus or irrelevant for this task
            ## NNP and NNPS are not very accurate, FW identifies some conventionalized abbreviations (et. al. and i.e.)
            ##     and latin terms (per se).  SYM cases are eliminated in other ways
            ## Punctuation cases are already ignored
            tagger_pos = None  # @semanticbeeng static type @todo !
        elif tagger_pos == 'NN':
            tagger_pos = 'NOUN'
        elif tagger_pos == 'NNS':
            tagger_pos = 'PLURAL'
        elif tagger_pos in ['TO', 'IN']:
            tagger_pos = 'PREP'
        elif tagger_pos in ['RB', 'RBR', 'RBS', 'RP', 'WRB']:
            tagger_pos = 'ADVERB'
        elif tagger_pos in ['JJ', 'JJR', 'JJS']:
            tagger_pos = 'ADJECTIVE'
        elif tagger_pos in ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'VB']:
            tagger_pos = 'VERB'
        elif tagger_pos in ['DT', 'PDT', 'WDT', 'PRP$', 'WP$', 'CD']:
            tagger_pos = 'DET'
        elif tagger_pos == 'POS':
            pass
        else:
            tagger_pos = 'OTHER'
    else:
        tagger_pos = None  # @semanticbeeng static type @todo !
    return tagger_pos

#
#
#
def divide_sentence_into_words_and_start_positions(sentence: str, start: int = 0) -> List[Tuple[int, str]]:
    ## only sequences of letters are needed for look up
    break_pattern: Pattern[str] = re.compile('[^0-9A-Za-z-]')
    match: Optional[Match[str]] = break_pattern.search(sentence, start)
    output: List[Tuple[int, str]] = []                                  # @semanticbeeng @todo static typing

    while match:
        if start != match.start():
            output.append((start, sentence[start:match.start()]))       # @semanticbeeng @todo static typing
        start = match.end()
        match = break_pattern.search(sentence, start)

    if start < len(sentence):
        output.append((start, sentence[start:]))                        # @semanticbeeng @todo static typing
    return (output)


#
#
#
def list_intersect(list1: List[str], list2: List[str]) -> bool:
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                return (True)
    return (False)


#
#
#
def get_integrated_line_attribute_value_structure_no_list(line: str, types: List[str]) -> Optional[Dict[str, str]]:

    start: int = line.find(' ')

    if start != -1:
        av_type = line[:start]
        output: Optional[Dict[str, str]] = {}
    else:
        av_type = None      # @semanticbeeng static type @todo
        output = None       # @semanticbeeng static type @todo

    if av_type in types:
        pattern: Optional[Match[str]] = attribute_value_from_fact.search(line, start)
        output['av_type'] = av_type
        while pattern:
            output[pattern.group(1)] = pattern.group(2).strip('"')
            start = pattern.end()
            pattern = attribute_value_from_fact.search(line, start)
    return (output)


#
# @semanticbeeng @todo gobal to object
#
def derive_plurals(word: str) -> List[str]:
    ## the dictionary plurals, actually includes -ing forms of verbs as well
    ## and regularizes them to verbs (which may or may not also be nouns)
    if word in dictionary.plural_dict:
        return (dictionary.plural_dict[word])
    elif len(word) <= 1:
        return ([])     # @semanticbeeng static type @todo
    elif (word[-1] in 'sxz') or (word[-2:] in ['sh', 'ch']):
        output = word + 'es'
    elif (word[-1] == 'y') and not (word[-2] in 'aeiou'):
        output = word[:-1] + 'ies'
    else:
        output = word + 's'
    return ([output])
    ## for more stringent use of plurals, add optional variable unigram_check
    ## and set it to True, uncomment the following line and all other unigram references
    # if (not unigram_check) or (output.lower() in unigram_dictionary):
    #     return([output])


#
# @semanticbeeng dead code
#
# def increment_unigram_dict_from_lines(lines):
#     for line in lines:
#         words = re.split('[^a-zA-Z]', line)
#         for word in words:
#             if word != '':
#                 unigram_dictionary.add(word.lower())


#
# @semanticbeeng dead code
#
# def save_unigram_dict(outfile):
#     global unigram_dictionary
#     with open(outfile, 'w') as outstream:
#         for word in unigram_dictionary:
#             outstream.write(word + os.linesep)


#
# @semanticbeeng dead code
#
# def load_unigram_dict(infile):
#     global unigram_dictionary
#     unigram_dictionary.clear()
#     with open(infile) as instream:
#         for line in instream:
#             unigram_dictionary.add(line.strip())


#
# @semanticbeeng dead code
#
# def get_n_random_lines(infile, outfile, N):
#     random.seed()
#     lines = open(infile).readlines()
#     output = []
#     while (len(output) < N) and (len(lines) > 0):
#         new_num = random.randint(0, len(lines) - 1)
#         output.append(lines.pop(new_num))
#     with open(outfile, 'w') as outstream:
#         for line in output:
#             outstream.write(line)


#
#
#
def merge_multiline_and_fix_xml(inlinelist: List[str]) -> List[str]:
    outlinelist: List[str] = []
    current_line: str = ''
    start_xml: Pattern[str] = re.compile('^[ \t]*<')
    for line in inlinelist:
        if start_xml.search(line) and (not '>' in line):
            current_line = current_line + line
        elif (current_line != ''):
            if ('>' in line):
                outlinelist.append(current_line + line)
                current_line = ''
            else:
                current_line = current_line + line
        else:
            outlinelist.append(line)
    if (current_line != ''):
        outlinelist.append(line)        # @semanticbeeng @todo
    return (outlinelist)


#
# @semanticbeeng use type FileName
#
def get_my_string_list(input_file: File) -> List[str]:
    try:
        instream = input_file.openText()
        output = instream.readlines()
    except:
        instream = input_file.openText(encoding='ISO-8859-1')
        output = instream.readlines()
    return (output)
