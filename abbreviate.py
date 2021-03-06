from term_utilities import *
from DataDef import File, TXT3, ABBR, AbbrT
from typing import List, Dict, Tuple, Pattern, Match, Optional
import dictionary
import config

# global abbr_to_full_dict          # @semanticbeeng @todo not used
# global full_to_abbr_dict
# global id_number
# global word_split_pattern
# global ABBREVIATION_STOP_WORDS
# global greek_match_table
# global number_match_table


word_split_pattern: Pattern[str] = re.compile(r'[^\w@]+')
ABBREVIATION_STOP_WORDS: List[str] = ['a', 'the', 'an', 'and', 'or', 'but', 'about', 'above', 'after', 'along', 'amid', 'among', 'as', 'at', 'by', 'for', 'from', 'in', 'into',
                                      'like',
                                      'minus', 'near', 'of', 'off', 'on', 'onto', 'out', 'over', 'past', 'per', 'plus', 'since', 'till', 'to', 'under', 'until', 'up', 'via', 'vs',
                                      'with',
                                      'that']

id_number: int = 0

#
#
#
class Abbreviate:
    abbr_to_full_dict: Dict[str, List[str]] = {}
    full_to_abbr_dict: Dict[str, List[str]] = {}

greek_match_table: Dict[str, str] = {'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Θ': 'T',
                     'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O',
                     'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'U', 'Φ': 'P', 'Χ': 'C', 'Ψ': 'P', 'ϖ': 'P'}

number_match_table: Dict[str, str] = {'ONE': '1', 'TWO': '2', 'THREE': '3', 'FOUR': '4', 'FIVE': '5', 'SIX': '6', 'SEVEN': '7', 'EIGHT': '8', 'NINE': '9', 'FIRST': '1', 'SECOND': '2',
                      'THIRD': '3', 'FOURTH': '4', 'FIFTH': '5', 'SIXTH': '6', 'SEVENTH': '7', 'EIGHTH': '8', 'NINTH': '9', 'UNI': '1', 'BI': '2', 'TRI': '3', 'QUAD': '4',
                      'QUINT': '5'}


#
#
#
def ill_formed_abbreviation_pattern(abbreviation_pattern: Match[str]) -> bool:
    ## attempts to identify parentheses that do not contain abbreviations
    ## first type is of the form (X,Y) (or (X,Y,Z,...) where X and Y are
    ## single characters
    ## 57
    token_list = re.split('[,;]', abbreviation_pattern.group(2))
    out = []
    if len(token_list) > 1:
        for token in token_list:
            token = token.strip(' ')
            if len(token) > 0:
                out.append(token)
    if len(out) > 1 and (len(out[0]) == 1) and (len(out[1]) == 1):
        return (True)
    else:
        return (False)


#
#
#
def regularize_match_string(string: str) -> str:
    return (re.sub('[- ]+', ' ', string.strip(''' ,.?><'";:][{}-_=)(*&^%$#@!~''').upper()))


#
#
#
def regularize_match_string1(string: str) -> str:
    return (re.sub('[-]', ' ', string.upper()))


#
#
#
def remove_empties(input_list: List[str]) -> List[str]:
    if type(input_list) == list:
        return ([x for x in input_list if (x != '')])
    else:
        raise ValueError('@refactoring: unexpected argument' + str(input_list))
        return (input_list)


#
#
#
def get_more_words(line: str, length: int) -> List[str]:
    ## print(line)
    ## print(length)
    if line and re.search('[^\W\d]', line):
        words: List[str] = remove_empties(word_split_pattern.split(line.strip(''' ,.?><'";:][{}-_=)(*&^%$#@!~''')))
        if len(words) > length:
            return (words[0 - length:])
        else:
            return (words)
    else:
        return ([])  # @semanticbeeng static type @todo


#
#
#
def ok_inbetween_abbreviation_string(string: str) -> bool:
    word_list = remove_empties(word_split_pattern.split(string))
    if len(word_list) < 3:
        return (True)
    else:
        return (False)


#
# @semanticbeeng @todo global state abbr_to_full_dict
#
def lookup_abbreviation(abbreviation: str, line: str, end: int, file_position: int, backwards_borders: List[int] = []) -> Optional[AbbrT]:
    if len(abbreviation) > 1 and abbreviation[0] in '\'"“`':
        abbreviation2 = abbreviation[1:]
        one_off = True
    else:
        one_off = False
        abbreviation2 = abbreviation

    if re.search('[-/]', abbreviation2):
        abbreviation2 = re.sub('[-/]', '', abbreviation2)

    key = abbreviation2.upper()
    output: Optional[AbbrT] = None
    search_string = regularize_match_string1(line[:end])
    maxlength = 0
    out_type = 'JARGON'

    if key in Abbreviate.abbr_to_full_dict:

        entry = Abbreviate.abbr_to_full_dict[key]
        ## print(entry)
        ## print(search_string)
        for out_string in entry:
            # add_s = False     @semanticbeeng not used @todo
            position = search_string.rfind(out_string)
            if backwards_borders and (position != -1):
                match_end = (position + len(out_string))
                len_difference = match_end - len(line)
                if len_difference > 0:
                    end = backwards_borders[1] + file_position - len_difference
                else:
                    end = backwards_borders[1] + file_position
                begin: int = backwards_borders[0] + file_position
                out_string = line[:match_end]

                output = AbbrT(begin, end, out_string, out_type, one_off)

            elif (position != -1):
                match_end = (position + len(out_string))

                if (match_end < len(search_string)) and (search_string[match_end] == 'S'):
                    add_s = True
                    match_end = 1 + match_end

                if (match_end < len(search_string)) and (re.search('[A-Z]', search_string[match_end])):
                    position = -1

                if position != -1:
                    out_string = line[position:match_end]
                    if ok_inbetween_abbreviation_string(search_string[position + len(out_string):]) and \
                            ((not output) or (len(out_string) > maxlength)):
                        maxlength = len(out_string)
                        begin = position + file_position
                        end = begin + len(out_string)
                        out_type = 'JARGON'

                        output = AbbrT(begin, end, out_string, out_type, one_off)
    return (output)


#
#
#
def adjust_start_for_antecedent(line: str, start: int, search_end: int) -> int:
    if start and search_end and (';' in line[start:search_end]):
        return (start + line[start:search_end].rindex(';'))
    else:
        return (start)


#
#
#
def blocked_abbreviation(line: str, abbreviation_position: int, abbreviation: str) -> bool:

    pattern = re.search('([^ ]) *$', line[:abbreviation_position])
    if pattern:
        previous_character = pattern.group(1)
        if previous_character == ';':
            ## semicolon always blocks abbreviation
            return (True)
        elif (previous_character == '.') and (len(abbreviation) == 1) and \
                (len(line) > abbreviation_position + 2) and (line[abbreviation_position + 2] == ')'):
            ## this identifies situations likely to be enumeration, e.g., (a) ... (b) ...
            ## further constraints may include requiring the letters to be lowercase, although
            ## it is unclear that this is necessary
            return (True)
        elif abbreviation.islower() and (abbreviation in ABBREVIATION_STOP_WORDS):
            return (True)
        elif abbreviation.istitle() and (abbreviation.lower() in ABBREVIATION_STOP_WORDS):
            return (True)
    return (False)       # @semanticbeeng @ todo static typing

#
#
#
def almost_the_same(word1: str, word2: str) -> bool:
    ## print(word1,word2)
    if (word1 == word2):
        return (True)
    if (word1 in word2) or (word2 in word1):
        ratio = len(word1) / len(word2)
        if abs(ratio - 1) <= .3:
            return (True)
        else:
            return (False)
    else:
        return (False)


#
#
#
def one_word_match_match(word: str, abbreviation: str) -> bool:

    if re.search('[A-Z]', abbreviation) and (len(word) > len(abbreviation) + 1) and \
            abbreviation.isalpha() and \
            (word[0].upper() == abbreviation[0].upper()):
        ## require first characters to match
        ## requires abbreviation to be at least 2 characters short than word
        ## requires abbreviation to contain at least one uppercase character
        ## require that the characters in the abbreviation after the first
        ## match in order, with any number of skips, but none are missed
        abbreviation_num = 1
        word_num = 1

        while (word_num < len(word)) and (abbreviation_num < len(abbreviation)):
            if word[word_num].upper() == abbreviation[abbreviation_num].upper():
                abbreviation_num = abbreviation_num + 1
            word_num = word_num + 1
        if abbreviation_num == len(abbreviation):
            return (True)
        else:
            return (False)
    return (False)       # @semanticbeeng @ todo static typing


#
#   @semanticbeeng @todo static typing
#
def match_abbreviation_chunk(word: str, abbreviation: str, whole: str=None) -> Optional[str]:

    ## print(word,abbreviation,whole)
    ## print(len(abbreviation),(.7 *len(word)))
    if whole and (almost_the_same(word.upper(), whole.upper())):
        ## whole provides the whole abbreviation if the test is against a portion
        ## of the original
        return (None)                   # @semanticbeeng @todo static typing
    substrings = []
    for num in range(len(abbreviation)):
        if abbreviation[0 - num].upper() == word[0].upper():
            substrings.append(abbreviation[(0 - num):])
    for num in range(len(substrings)):
        substring = substrings[0 - num]
        if one_word_match_match(word, substring):
            ## print('1',word,'2',abbreviation,'3',substring)
            return (substring)
    return (None)                      # @semanticbeeng @todo static typing


#
#
#
def get_position_before_word(word: str, line: str) -> Optional[int]:
    pattern = re.search(r'[^\w@]+' + word + '[^\w@]*$', line)
    if pattern:
        return (pattern.start() + 1)

    return (None)       # @semanticbeeng @ todo static typing


#
#
#
def unbalanced_delimiter(outstring: str) -> bool:
    ## This will be False if there are no delimiters (brackets), or if
    ## there is a left and right delimiter, such that the left
    ## precedes the right.
    ## This will return True if there is a left not followed by a right
    ## or a right that is not preceded by a left (i.e., exactly one delimiter
    ## or a delimiter out of order).    
    left = re.search('[(\[{"]', outstring)
    if left and len(outstring) > left.start():
        right = re.search('[)\]}"]', outstring[left.start() + 1:])
        if right:
            return (False)
        else:
            return (True)
    elif re.search('[)\]}]', outstring):
        return (True)
    else:
        return (False)


#
#
#
def fix_unbalanced(outstring: str, line: str, line_position: int) -> Optional[Tuple[int, str]]:
    ## print(outstring,line,line_position,sep=os.linesep)
    ## this balances parens for formulaic items that contain parens
    ## the good ones all have hyphens either before the left paren
    ## or after the right one
    ## print(outstring,line,line_position,sep=os.linesep)
    right = re.search('[)\]}]', outstring)
    quote = re.search('"', outstring)

    if right:
        character_position = re.search('([^ ]+) *$', line[:line_position])
        if character_position and re.search('[{\[(]', character_position.group(1)):
            new_start = character_position.start(1)
            new_string = line[new_start:line_position] + outstring
            if re.search('(-[(\[{])|([)\]}]-)', new_string):
                return (new_start, new_string)
            else:
                return (None, None)             # @semanticbeeng @todo static typying
        else:
            return (None, None)                 # @semanticbeeng @todo static typying

    elif quote:
        ## evaluates to True if out is found
        ## print(quote.start(),quote.group(0))
        if len(outstring) > quote.start() and not (re.search('"', outstring[quote.start() + 1:])):
            character_position = re.search('([^ ]+) *$', line[:line_position])
            if character_position and re.search('"', character_position.group(1)):
                new_start = character_position.start(1)
                new_string = line[new_start:line_position] + outstring
                return (new_start, new_string)
            else:
                return (None, None)             # @semanticbeeng @todo static typying
        else:
            return (None, None)                 # @semanticbeeng @todo static typying
    else:
        return (None, None)                     # @semanticbeeng @todo static typying


#
#   @semanticbeeng @todo static typing
#
def get_word_substring_at_end(words: List[str], line: str, inbetween: Optional[str]=None, no_check: bool=False) -> Optional[Tuple[str, int]]:
    ## this assumes that the words occur at the end of the line
    ## and that any characters ignored (hyphens, numbers, etc.) 
    ## are OK to ignore
    if inbetween:
        if re.search('[)\]}]', inbetween):
            ## the match is discarded if right brackets appear
            ## in between the abbreviation and antecedent
            return (None, None)               # @semanticbeeng @todo static typying
        elif (line[-1] == ' '):
            inbetween = None                  # @semanticbeeng @todo static typying
        elif len(inbetween) == 1 and inbetween[0] in '([':
            inbetween = None                  # @semanticbeeng @todo static typying
        elif ' ' in inbetween:
            if inbetween[0] == ' ':
                inbetween = None              # @semanticbeeng @todo static typying
            else:
                inbetween_space = inbetween.index(' ')
                inbetween = inbetween[:inbetween_space]

    line_upper = line.upper().rstrip(' ')
    line_position = len(line_upper)
    not_found = False

    for number in range(len(words)):
        word_position = -1 - number
        word = words[word_position]
        word = word.upper()
        if word in line_upper[0:line_position]:
            line_position = line_upper.rindex(word, 0, line_position)
        else:
            not_found = True
            break

    if not_found:
        outstring = None                        # @semanticbeeng @todo static typying
    else:
        outstring = line[line_position:]

    if outstring and inbetween:
        outstring = outstring + inbetween
        outstring = outstring.rstrip(' ')

    if outstring and unbalanced_delimiter(outstring) and (not no_check):
        ## if there is a left or right bracket, but not both
        ## this is ill-formed
        new_position, outstring = fix_unbalanced(outstring, line, line_position)
        if new_position:
            line_position = new_position
    if not outstring:
        return (None, None)                   # @semanticbeeng @todo static typying
    else:
        return (outstring, line_position)


#
#
#
def letter_match(char1: str, word: str) -> bool:
    ## char 1 is from the abbreviation
    char2 = word[0]
    ## char 2 is from the word
    if (char1 == char2):
        return (True)
    if (char1 in greek_match_table) and (greek_match_table[char1] == char2):
        return (True)
    elif (char2 in greek_match_table) and (greek_match_table[char2] == char1):
        return (True)
    elif (char1 == 'X') and (len(word) > 2) and (word[:2] == 'EX'):
        return (True)
    elif char1.isdigit() and (word in number_match_table) and (number_match_table[word] == char1):
        return (True)
    else:
        return (False)


#
# @semanticbeeng static type @todo
#
def classify_abbreviated_string(word_string: str, wordlist: List[str] = []) -> str:
    if not wordlist:
        wordlist = remove_empties(word_split_pattern.split(word_string))
    if '@' in word_string:
        return ('EMAIL')
    elif re.search('(http)|(www)', word_string.lower()):
        return ('URL')
    for word in wordlist:
        if (organization_word_pattern.search(word)):
            return ('ORGANIZATION')
    if word_string.upper() in dictionary.location_dictionary:
        return ('GPE')
    might_be_gpe = True
    has_gpe_word = False

    for word in wordlist:
        if word.upper() in dictionary.location_dictionary:
            has_gpe_word = True
        elif not (word.lower()) in ABBREVIATION_STOP_WORDS:
            might_be_gpe = False
    if might_be_gpe and has_gpe_word:
        return ('GPE')
    return ('JARGON')


#
#
#
def abbreviation_match(abbreviation: str, previous_words: List[str], line: str, abbreviation_position: int,
                       line_offset: int     # @semanticbeeng @todo not used previous_line: List[str], more_words: bool
                       ) -> Optional[AbbrT]:
    ## Missing cases: 1) "A recombinant form of SPARC (rSPARC)" -- not general -- not clear what we can skip
    ##                2) ADAMTS-2 (A Disintegrin And Metalloproteinase with ThromboSpondin motifs)  ## also not clear -- when can we add a number
    ##                3) tetracycline (tet) -- not completely clear because we get similar cases, but perhaps it is the length
    one_off = False
    out_string: Optional[str] = None        # @semanticbeeng static type @todo
    matching_words: List[str] = []
    # organization = False                  @semanticbeeng not used
    abbreviation2 = abbreviation
    skipped_maximum = 3
    stop_words = 0
    skipped_words = 0
    trimmed_words = 0
    last_word_was_stop_word = None          # @semanticbeeng static type @todo
    pattern_that_matched: int = None        # @semanticbeeng static type @todo
    final_s = False
    final_match = False
    # multi_letter = False

    if len(abbreviation) > 1 and abbreviation[0] in '\'"“`':
        one_off = True
        abbreviation2 = abbreviation[1:]

    if re.search('[-/]', abbreviation2):
        abbreviation2 = re.sub('[-/]', '', abbreviation2)

    if blocked_abbreviation(line, abbreviation_position, abbreviation) \
            or not (re.search('[^\W\d]', abbreviation2)) or \
            ((len(abbreviation2) == 1) and not (re.search('[A-Z]', abbreviation2))):
        ## initially just covers semi-colon and enumeration cases
        ## also requires that abbreviations contain letters
        ## and that single character abbreviations be a capial letter
        return (None)                       # @semanticbeeng static type @todo

    if not re.search('[^\W\d]', abbreviation2):
        Fail = True
    else:
        Fail = False

    if not Fail:
        ## abbreviations must contain at least one letter
        all_matches = True
        number = 0
        extra_letters = 0
        word_index = 0

        while (((number < len(abbreviation2)) and (not final_s)) or
                   (final_s and (number + 1 < len(abbreviation2)))) and \
                all_matches and (len(previous_words) > ((stop_words + skipped_words + number) - extra_letters)):

            if (number == 0) and \
                    (len(previous_words) > 1) and (len(abbreviation2) > 1) and \
                    (abbreviation2[-1] in ['s', 'S']) and \
                    (previous_words[-1][-1] in ['s', 'S']) and \
                    (not previous_words[-1][0] in ['s', 'S']):
                final_s = True

            if final_s:
                index = -2 - number
                word_index = 1 + (index - ((stop_words + skipped_words) - extra_letters))
            else:
                index = -1 - number
                word_index = index - ((stop_words + skipped_words) - extra_letters)

            if letter_match(abbreviation2[index].upper(), previous_words[word_index].upper()):
                if previous_words[word_index].lower() in ABBREVIATION_STOP_WORDS:
                    last_word_was_stop_word = previous_words[word_index]
                else:
                    last_word_was_stop_word = None      # @semanticbeeng @todo static typing
                number = number + 1

                if (number == len(abbreviation2)) or (final_s and ((1 + number) == len(abbreviation2))):
                    final_match = True

            elif last_word_was_stop_word and (last_word_was_stop_word[0].upper() == previous_words[word_index][0].upper()):
                last_word_was_stop_word = None         # @semanticbeeng @todo static typying
                stop_words = stop_words + 1
                if number == 0:
                    trimmed_words = trimmed_words + 1

            elif previous_words[word_index].lower() in ABBREVIATION_STOP_WORDS:
                stop_words = stop_words + 1
                if number == 0:
                    trimmed_words = trimmed_words + 1
                last_word_was_stop_word = previous_words[word_index]

            else:
                if index == -1:  ## end of the word is special for Python
                    possible_match = match_abbreviation_chunk(previous_words[word_index].strip('''"'.,'''), abbreviation2)
                    # end_of_ab = True
                else:
                    possible_match = match_abbreviation_chunk(previous_words[word_index].strip('''"'.,'''), abbreviation2[:index + 1], abbreviation2)
                    # end_of_ab = False

                if possible_match:
                    number = number + len(possible_match)

                    if number == len(abbreviation2):
                        final_match = True
                    extra_letters = extra_letters + (len(possible_match) - 1)
                    # multi_letter = True

                elif (len(abbreviation2) > 2) and (len(abbreviation2) > (skipped_words + 1)) and (skipped_words < skipped_maximum):
                    skipped_words = 1 + skipped_words
                    if number == 0:
                        trimmed_words = trimmed_words + 1
                else:
                    all_matches = False
        if all_matches and (not final_match):
            ### 57 
            all_matches = False
        if all_matches:
            if final_s:
                if (len(previous_words) + 1 + extra_letters) < (stop_words + skipped_words + number):
                    all_matches = False
            elif (len(previous_words) + extra_letters) < (stop_words + skipped_words + number):
                all_matches = False
        if all_matches:
            pattern_that_matched = 1
            if final_s:
                matching_words = previous_words[1 - (len(abbreviation2) + (stop_words + skipped_words) - extra_letters):]
            else:
                matching_words = previous_words[0 - (len(abbreviation2) + (stop_words + skipped_words) - extra_letters):]
            end_position = abbreviation_position

            if trimmed_words > 0:
                for num in range(trimmed_words):
                    if end_position:
                        end_position = get_position_before_word(previous_words[0 - (1 + num)], line[:end_position])
                        ## subtract the length of the words removed from the end of the list of words
                        ## also subtract one for the space (or other delimiter)
                if end_position:
                    matching_words = matching_words[:(0 - trimmed_words)]

            out_string, start_position = get_word_substring_at_end(matching_words, line[:end_position], line[end_position:abbreviation_position])

            if out_string:
                begin = line_offset + start_position
                end = begin + len(out_string)

    if out_string and (len(out_string) <= (len(abbreviation2) + 1)):
        out_string = None                  # @semanticbeeng @todo static typying
        all_matches = False
        Fail = True

    if (not out_string) and (not Fail):
        ## special case: one of the previous words is itself an allcaps abbreviation,
        ## typically the last one:  small interfering RNA (siRNA)
        ## Note: This version does not account for stop words  *****************
        allcap_word: str = None                 # @semanticbeeng @todo static typing
        word_number = 0
        ab_index: Optional[int] = None          # @semanticbeeng @todo static typying

        for num in range(min(len(previous_words), len(abbreviation2) - 1)):
            word_num = -1 - num
            word = previous_words[word_num]
            if word.isupper() and not allcap_word:
                ab_index = abbreviation2.upper().find(word)
                if ab_index != -1:
                    allcap_word = word

        if allcap_word and allcap_word != abbreviation2 and (len(abbreviation2) > len(allcap_word)) and len(previous_words) > 1:
            all_matches = True
            chosen_words: List[str] = []
            if (ab_index == 0):  ## allcaps is at beginning of abbreviation

                for number in range(len(abbreviation2) - len(allcap_word)):
                    index = -1 - number
                    if all_matches and (abs(index) <= len(previous_words)) and \
                            (not letter_match(abbreviation2[index].upper(), previous_words[index].upper())):
                        all_matches = False

                if all_matches:
                    chosen_words = previous_words[(len(allcap_word) - len(abbreviation2) - 1):]
                    matching_words.append(allcap_word)
                    matching_words.extend(chosen_words)

            elif (ab_index + len(allcap_word)) == len(abbreviation2):  ## allcaps is at end of abbreviation
                for number in range(len(abbreviation2) - len(allcap_word)):
                    abbreviation_index = -1 - (len(allcap_word)) - number
                    word_index = 0 - 2 - number
                    if all_matches and (len(abbreviation2) > abbreviation_index) and \
                            (len(previous_words) >= abs(word_index)) and (previous_words[word_index] != '') and \
                            (not letter_match(abbreviation2[abbreviation_index].upper(), previous_words[word_index].upper())):
                        all_matches = False

                if all_matches:
                    chosen_words = previous_words[word_index:]  ## last value of word_index
                    matching_words = []
                    matching_words.extend(chosen_words)

            if all_matches:
                pattern_that_matched = 3
                out_string, start_position = get_word_substring_at_end(chosen_words, line[:abbreviation_position])
                if out_string:
                    begin = line_offset + start_position
                    end = begin + len(out_string)

    if (not out_string) and (not Fail):
        if len(previous_words) > 0 and one_word_match_match(previous_words[-1], abbreviation2):
            matching_words = previous_words[-1:]
            pattern_that_matched = 5
            out_string, start_position = get_word_substring_at_end(matching_words, line[:abbreviation_position])
            if out_string:
                begin = line_offset + start_position
                end = begin + len(out_string)

        elif len(previous_words) >= 2 and len(previous_words[-1]) <= 2 and len(abbreviation2) > 2 and \
                abbreviation2.endswith(previous_words[-1]) and \
                one_word_match_match(previous_words[-2], abbreviation2[:-1]):
            pattern_that_matched = 6
            matching_words = previous_words[-2:]
            out_string, start_position = get_word_substring_at_end(matching_words, line[:abbreviation_position])

            if out_string:
                begin = line_offset + start_position
                end = begin + len(out_string)
                ## if abbreviation consists of N consonants and an optional number, and those N consonants are the first N
                ## consonants in the first word of the match and the optional number is the second match
                ## examples: peroxiredoxin (Prx) and thioredoxin 1 (Trx1)
    if out_string:
        output_type = classify_abbreviated_string(out_string, wordlist=matching_words)

    if matching_words and out_string and (not Fail):
        if (len(out_string) > 1) and (out_string[1] in '''`'"“"”'''):
            out_string = out_string[1:]
            begin = begin + 1
        if (len(out_string) > 1) and (out_string[-1] in '''`'"“"”'''):
            out_string = out_string[:-1]
            end = end - 1

        return AbbrT(begin, end, out_string, output_type, one_off)

    return (None)       # @semanticbeeng @ todo static typing

#
#
#
def bad_jargon(jargon: str) -> Optional[Match[str]]:
    return (re.search('(19[89][0-9])|(20[01][0-9])|[\[=]|((^| )and($| ))|[\[\]:“"”\`\'‘]', jargon))


#
#
#
def OK_jargon(jargon: str) -> bool:
    return ((type(jargon) == str) and (len(jargon) > 1) and
           (re.search('[^\W\d]', jargon)) and          # @semanticbeeng @todo static typing
           (not bad_jargon(jargon)))


#
#
#
def OK_abbrev_antec(anteced):
    words = re.split('[ .-]+', anteced)
    all_one_letter = True
    left_parens = anteced.count('(')
    right_parens = anteced.count(')')
    for word in words:
        if len(word) > 1:
            all_one_letter = False
    return ((not all_one_letter) and (left_parens == right_parens) \
            and (left_parens < 2) and (right_parens < 2))


def get_next_id_number():
    global id_number
    id_number = 1 + id_number
    return (id_number)


#
#   @semanticbeeng @todo generate unique ids in a cluster
#
def make_nyu_id(Class: str) -> str:
    number = get_next_id_number()
    return ('NYU_' + Class + str(number))


#
#
#
def make_nyu_entity(entity_type: str, string: str, begin: int, end: int) -> Dict[str, str]:
    if entity_type == 'JARGON':
        return ({'CLASS': entity_type, 'ID': make_nyu_id(entity_type),
                 'START': begin, 'END': end, 'TEXT': string})
    elif entity_type in ['ORGANIZATION', 'PERSON', 'URL', 'EMAIL', 'GPE']:
        return ({'CLASS': 'ENAMEX', 'TYPE': entity_type, 'ID': make_nyu_id('ENAMEX'),
                 'START': begin, 'END': end, 'TEXT': string})
    else:
        print(1, string, begin, end)
        print('No such entity type:', entity_type)
        raise ValueError('No such entity type:' + entity_type)


#
#
#
def extend_abbreviation_context(pattern: Optional[Match[str]], line: str) -> bool:
    end = pattern.end()
    if len(line) > end:
        next_character = line[end]
        if next_character in '-':
            ## possibly find other bad next characters
            return (True)
    return (False)


#
#
#
def find_search_end(line: str, search_end: int) -> Tuple[int, bool]:
    Fail = False
    pattern = re.search('[\w][\W]+$', line[:search_end])
    if pattern:
        if re.search(r'[!:;,.?)\]}]', line[pattern.start():search_end]):
            # the parentheses pattern does not work if there is
            # sentence delimiting or conjunct delimiting punctuation
            # between antecedent and left parenthesis
            Fail = True
        return ((pattern.start() + 1), Fail)
    else:
        return (search_end, Fail)


#
#
#
def invalid_abbreviation(ARG2_string: str) -> bool:
    if not isinstance(ARG2_string, str):
        return (True)

    elif ARG2_string.islower() and \
            ((ARG2_string in config.pos_dict) or (ARG2_string in config.nom_dict)):
        return (True)

    elif ARG2_string.istitle() and \
            ((ARG2_string.lower() in config.pos_dict) or (ARG2_string.lower() in config.nom_dict)
             or ((ARG2_string.lower() in dictionary.location_dictionary)
             and (not 'ABBREVIATION-OF' in dictionary.location_dictionary[ARG2_string.lower()]))):
        return (True)

    elif ARG2_string.isupper() and roman(ARG2_string):
        return (True)

    return (False)


#
#
#
def invalid_abbrev_of(ARG2_string, ARG1_string, recurs=False) -> bool:
    if (ARG2_string == '') or (ARG1_string == ''):
        return (True)

    elif ' ' in ARG1_string:
        return (False)  ## these errors are only for single word cases

    elif (not recurs) and (ARG2_string[-1] in 'sS') and (ARG1_string[-1] in 'sS') \
            and (not invalid_abbrev_of(ARG2_string[:-1], ARG1_string[:-1], recurs=True)):
        ## handles plurals
        return (False)

    elif ARG1_string.lower().startswith(ARG2_string.lower()):
        return (False)  ## prefixes are valid 1 word abbreviations

    elif (len(ARG2_string) == 2) and (ARG2_string[0].lower() == ARG1_string[0].lower()) \
            and (ARG2_string[-1].lower() == ARG1_string[-1].lower()):
        return (False)  ## first and last character matches are valid abbreviations

    else:
        string_index = 0
        abbrev_index = 0
        string = ARG1_string.lower()
        abbrev = ARG2_string.lower()
        # OK = True
        string_type: str = None         # @semanticbeeng static type
        string_char: str = None
        match = False
        next_type: str = None           # @semanticbeeng static type

        while (string_index < len(string)) and (abbrev_index < len(abbrev)):
            ## match initial consonant and vowel clusters
            last_type = string_type
            last_match = match
            string_char = string[string_index]
            abbrev_char = abbrev[abbrev_index]
            if string_char == abbrev_char:
                match = True
            else:
                match = False
            if string_char in 'aeiou':
                string_type = 'vowel'
            else:
                string_type = 'consonant'
            if (string_index < (len(string) - 1)):
                if string[string_index + 1] in 'aeiou':
                    next_type = 'vowel'
                else:
                    next_type = 'consonant'
            else:
                next_type = None        # @semanticbeeng static type

            # print(1,string_char,abbrev_char,match,string_type)
            # print(2,last_type,last_match)
            # print(3,abbrev_index)
            if match and (last_match or (last_type != string_type) \
                                  or ((string_type == 'consonant') and (next_type == 'vowel'))):
                ## looking for match and vowel/consonant cluster border
                ## abbrev char can be vowel following consonant
                ## or consonant that is either preceded or followed by a vowel
                abbrev_index = abbrev_index + 1
            string_index = string_index + 1
        #        print('final',string_index,len(string),abbrev_index,len(abbrev))
        if abbrev_index == len(abbrev):
            return (False)
        else:
            return (True)


#
#
#
def get_next_abbreviate_relations(previous_line: str, line: str, position: int) -> List[Dict[str, str]]:
    global word_split_pattern
    output: List[Dict[str, str]] = []
    start = 0
    pattern: Optional[Match[str]] = parentheses_pattern_match(line, start, 2)
    ### parentheses_pattern2.search(line,start)
    ## allows for unclosed parenthesis
    more_words: List[str] = []          # @semanticbeeng static type @ todo

    ARG1_begin: int                     # @semanticbeeng static type @ todo
    ARG1_end: int                       # @semanticbeeng static type @ todo

    ARG2_begin: int                     # @semanticbeeng static type @ todo
    ARG2_end: int                       # @semanticbeeng static type @ todo

    ARG2_string: str                    # @semanticbeeng static type @ todo
    output_type: str                    # @semanticbeeng static type @ todo

    # result: Optional[Abbr] = None     # @semanticbeeng static type @ todo
    Fail = False
    extend_antecedent: bool = False     # @semanticbeeng static type @ todo
    last_start: int = None              # @semanticbeeng static type @ todo
    alt_abbreviation: str = None        # @semanticbeeng static type @ todo

    while pattern:
        result: Optional[AbbrT] = None   # @semanticbeeng static type @ todo
        Fail = False
        first_word_break: Optional[Match[str]] = re.search('[^\(]([ ,;:])', pattern.group(2))

        if first_word_break:
            abbreviation = pattern.group(2)[:first_word_break.start(1)]
        else:
            abbreviation = pattern.group(2)

        if abbreviation:
            abbrev_start = re.search('[^ /-]', abbreviation)
            if abbrev_start and (abbrev_start.start() > 0):
                alt_abbreviation = abbreviation[abbrev_start.start():]
        ## whole pattern goes from ( to ) 
        ## 1st guess at abbreviation is the portion that is after (
        ## and is either: before the first space; or the whole thing
        ## if there is no space
        search_end = pattern.start()
        search_end, Fail = find_search_end(line, search_end)

        if ill_formed_abbreviation_pattern(pattern):
            Fail = True
            Double_Fail = True
        else:
            Double_Fail = False

        if re.search('^[a-zA-Z]$', abbreviation):
            ## eliminate ill_formed pattern plus all single roman letter abbreviations
            ## the latter are correct sometimes, but rarely useful at all for our purposes
            ## also eliminate cases where the parenthesized item is part of a complex formula of some sort
            ## (wrong abbreviation context)
            Fail = True

        if Fail and (not Double_Fail) and alt_abbreviation and (not re.search('^[a-zA-Z]$', alt_abbreviation)):
            abbreviation = alt_abbreviation
            alt_abbreviation = None        # @semanticbeeng static type
            Fail = False

        if not Fail:
            if extend_antecedent:
                start = adjust_start_for_antecedent(line, last_start, search_end)
            else:
                start = adjust_start_for_antecedent(line, start, search_end)

            previous_words: List[str] = remove_empties(word_split_pattern.split(line[start:search_end].rstrip(' ')))

            if (start == 0) and (previous_line != '') and (len(previous_words) < len(abbreviation)):
                more_words = get_more_words(previous_line, (3 + len(abbreviation) - len(previous_words)))

            if more_words and (len(more_words) > 0) and (len(abbreviation) > 0):
                offset_adjustment = len(previous_line)
                more_words.extend(previous_words)

                result = lookup_abbreviation(abbreviation, previous_line + line, search_end + offset_adjustment, position - offset_adjustment)

                if alt_abbreviation and (not result):

                    result = lookup_abbreviation(alt_abbreviation, previous_line + line, search_end + offset_adjustment, position - offset_adjustment)
                    if result:
                        abbreviation = alt_abbreviation

                if not result:
                    ## print(1,start,search_end)
                    result = abbreviation_match(abbreviation, more_words, previous_line + line, search_end + offset_adjustment, position - offset_adjustment
                                                # @semanticbeeng @todo not used , False, False
                                                )

                if (not result) and alt_abbreviation:
                    result = abbreviation_match(alt_abbreviation, more_words, previous_line + line, search_end + offset_adjustment, position - offset_adjustment
                                                # @semanticbeeng @todo not used , False, False
                                                )
                    if result:
                        abbreviation = alt_abbreviation

            if (not result) and (len(previous_words) > 0) and (len(abbreviation) > 0):

                result = lookup_abbreviation(abbreviation, line, search_end, position)

                if not result:
                    ## print(2,start,search_end)
                    result = abbreviation_match(abbreviation, previous_words, line, search_end, position
                                                # @semanticbeeng @todo not used  , False, False
                                                )

                if not result and alt_abbreviation:
                    result = lookup_abbreviation(abbreviation, line, search_end, position)
                    if not result:
                        result = abbreviation_match(alt_abbreviation, previous_words, line, search_end, position
                                                    # @semanticbeeng @todo not used , False, False
                                                    )
                    if result:
                        abbreviation = alt_abbreviation
            ## print(result)

            if result and ((not OK_jargon(result[2])) or (not OK_abbrev_antec(result[2]))):
                result = None          # @semanticbeeng static type

            if result:
                if result[4]:  ## if the abbreviation is one off
                    ARG2_begin = pattern.start() + position + 2
                    ARG2_string = abbreviation[1:]
                    ARG2_end = ARG2_begin + len(abbreviation) - 1
                else:
                    ARG2_begin = pattern.start() + position + 1
                    ARG2_string = abbreviation
                    ARG2_end = ARG2_begin + len(abbreviation)

                # @semanticbeeng @todo use Abbr explicitly
                ARG1_begin = result[0]
                ARG1_end = result[1]
                ARG1_string = result[2]
                output_type = result[3]

            elif len(abbreviation) == 1:
                ## single capital letters divided by spaces, are an alternative match, e.g., (J R A)
                ## Abbreviations can also contain periods
                ## -- we will try removing up to 7 spaces/periods
                abbreviation = re.sub('[. ]', '', pattern.group(2), 7)  ## remove upto 7 spaces/periods from abbreviation

                if (start == 0) and (previous_line != '') and (len(previous_words) < len(abbreviation)):

                    more_words = get_more_words(previous_line, (1 + len(abbreviation) - len(previous_words)))

                    if more_words and (len(more_words) > 0):
                        offset_adjustment = len(previous_line)
                        more_words.extend(previous_words)

                        result = lookup_abbreviation(abbreviation, previous_line + line, search_end + offset_adjustment, position - offset_adjustment)

                        if not result:
                            ## print(3)
                            result = abbreviation_match(abbreviation, more_words, previous_line + line, search_end + offset_adjustment, position - offset_adjustment
                                                        # @semanticbeeng @todo not used , False, False
                                                        )

                    else:
                        result = lookup_abbreviation(abbreviation, line, search_end, position)
                        ## print(4)
                        if not result:
                            result = abbreviation_match(abbreviation, previous_words, line, search_end, position,
                                                        # @semanticbeeng @todo not used previous_line, more_words
                                                        )

                if result:
                    if result[4]:
                        ARG2_begin = pattern.start() + position + 2
                        ARG2_string = abbreviation[1:]
                    else:
                        ARG2_begin = pattern.start() + position + 1
                        ARG2_string = pattern.start(2)

                    ARG2_end = start + pattern.end() - 1
                    ARG1_begin = result[0]
                    ARG1_end = result[1]
                    ARG1_string = result[2]
                    output_type = result[3]

            elif ' ' in pattern.group(0):
                ## possibility of a multi-word item in parentheses (antecedent) matching the word right before
                ## the parentheses (abbreviation), i.e., the backwards case
                # @semanticbeeng static type @todo previous_word: Optional[Match] = None
                if pattern.end() > 3:
                    previous_word: Optional[Match[str]] = re.search('([a-zA-ZΑ-ϖ][a-zA-Z0-9-/Α-ϖ]*[a-zA-Z0-9Α-ϖ])[^a-z0-9]$', line[:pattern.start()])
                else:
                    previous_word = None         # @semanticbeeng static type @todo

                if previous_word:
                    abbreviation = previous_word.group(1)
                    antecedent_string = pattern.group(0)[1:-1]

                    result = lookup_abbreviation(abbreviation, antecedent_string, len(pattern.group(0)) - 2, position,
                                                 backwards_borders=[previous_word.start(), pattern.end()])

                    if not result:
                        forward_words = remove_empties(word_split_pattern.split(antecedent_string.rstrip(' ')))
                        line_offset = len(pattern.group(0)) - 2
                        ## line_offset effects begin and end
                        ## *** 57 ***
                        result = abbreviation_match(abbreviation, forward_words, antecedent_string, line_offset, position
                                                    # @semanticbeeng @todo not used , previous_line, more_words
                                                    )

                    if result:
                        ARG1_string = result[2]
                        ARG2_string = abbreviation
                        ARG1_begin = pattern.start() + position + 1
                        ARG1_end = ARG1_begin + len(ARG1_string)  ## result[1]-1
                        ARG2_begin = previous_word.start() + position  ## result[0] ## correct for lookup, but not for calculated
                        ARG2_end = ARG2_begin + len(ARG2_string)
                        output_type = result[3]
                        ## must adjust offsets for backwards situation
                        ## perhaps provide offsets explicitly (start position = start of first word + offset)
                        ## end position = end position of pattern + offset

            if result:
                if not invalid_abbreviation(ARG2_string) and not invalid_abbrev_of(ARG2_string, ARG1_string):

                    #
                    #   @semanticbeeng @todo extract @data entity definitions
                    #
                    ARG2: Dict[str, str] = make_nyu_entity(output_type, ARG2_string, ARG2_begin, ARG2_end)
                    ARG1: Dict[str, str] = make_nyu_entity(output_type, ARG1_string, ARG1_begin, ARG1_end)

                    relation_start: int = min(ARG1_begin, ARG2_begin)
                    relation_end: int = max(ARG1_end, ARG2_end)

                    output.extend([ARG1, ARG2,
                                   {'CLASS': 'RELATION', 'TYPE': 'ABBREVIATE', 'ID': make_nyu_id('RELATION'),
                                    'START': relation_start, 'END': relation_end,
                                    'ARG1': ARG1['ID'], 'ARG2': ARG2['ID'],
                                    'ARG1_TEXT': ARG1_string, 'ARG2_TEXT': ARG2_string, 'GRAM_SIGNAL': 'PARENTHESES'}])
                    ## not currently using context_string or context

        if not result:
            start = pattern.start() + 1
        else:
            last_start = start
            start = pattern.end()

        if extend_abbreviation_context(pattern, line):
            extend_antecedent = True
        else:
            extend_antecedent = False

        pattern = parentheses_pattern_match(line, start, 2)
        ## pattern = parentheses_pattern2.search(line,start)

    # import json
    # print("############ ")
    # print("get_next_abbreviate_relations ======>>>>>>>> " + json.dumps(output))
    # print("############ ")
    return (output)


#
#
#
def record_abbreviate_dictionary(fulltext: str, abbreviation: str) -> None:
    ## print(fulltext,abbreviation,argclass)
    # global abbr_to_full_dict
    # global full_to_abbr_dict
    ### also need to update full_to_abbr_dict *** 57 ***
    key = abbreviation  ## use naturally occuring form of abbreviations (otherwise causes problems, e.g., if abbreviation is OR
    value = regularize_match_string1(fulltext)

    if key in Abbreviate.abbr_to_full_dict:
        if not value in Abbreviate.abbr_to_full_dict[key]:
            Abbreviate.abbr_to_full_dict[key].append(value)
    else:
        Abbreviate.abbr_to_full_dict[key] = [value]

    if value in Abbreviate.full_to_abbr_dict:
        if not key in Abbreviate.full_to_abbr_dict[value]:
            Abbreviate.full_to_abbr_dict[value].append(key)                # @semanticbeeng @todo @arch global state mutation
    else:
        Abbreviate.full_to_abbr_dict[value] = [key]                        # @semanticbeeng @todo @arch global state mutation


#
# @semanticbeeng other than `ABBREVIATE`, none of these strings is referenced in code
# @semanticbeeng @todo encapsulate
#
ARG1_NAME_TABLE: Dict[str, str] = {'EXEMPLIFY': 'SUBCLASS', 'DISCOVER': 'INVENTOR', 'MANUFACTURE': 'MAKER', 'SUPPLY': 'SUPPLIER',
                                   'ORIGINATE': 'INVENTOR', 'ALIAS': 'FULLNAME', 'ABBREVIATE': 'FULLNAME', 'BETTER_THAN': 'BETTER',
                                   'BASED_ON': 'DERIVED', 'CONTRAST': 'THEME', 'CORROBORATION': 'THEME', 'CO-CITATION': 'THEME',
                                   'POSITIVE': 'JUDGE', 'NEGATIVE': 'JUDGE', 'SIGNIFICANT': 'JUDGE', 'PRACTICAL': 'JUDGE', 'STANDARD': 'JUDGE', 'EMPHASIZED_TERM': 'THEME', 'COMPONENT': 'PART',
                                   'FEATURE': 'FEATURE'}

ARG2_NAME_TABLE: Dict[str, str] = {'EXEMPLIFY': 'SUPERCLASS', 'DISCOVER': 'INVENTION', 'MANUFACTURE': 'PRODUCT', 'SUPPLY': 'PRODUCT',
                                   'ORIGINATE': 'INVENTION', 'ALIAS': 'FULLNAME', 'ABBREVIATE': 'SHORTNAME', 'BETTER_THAN': 'WORSE',
                                   'BASED_ON': 'ORIGINAL', 'CONTRAST': 'THEME', 'CORROBORATION': 'THEME', 'CO-CITATION': 'THEME',
                                   'POSITIVE': 'THEME', 'NEGATIVE': 'THEME', 'SIGNIFICANT': 'THEME', 'PRACTICAL': 'THEME', 'STANDARD': 'THEME', 'EMPHASIZED_TERM': 'THEME', 'COMPONENT': 'WHOLE',
                                   'FEATURE': 'BEARER'}

#
# Serializes and persists a list of Fact entities
# @semanticbeeng @todo define FACT entity: is that different than ABBR?
#
def write_fact_file(output: List[Dict[str, str]], outfile: File[ABBR]) -> None:
    global ARG1_NAME_TABLE
    global ARG2_NAME_TABLE
    # global FACT_STYLE @semanticbeeng not used

    keys = ['ID', 'TYPE', 'SUBTYPE', 'START', 'END', 'ARG1', 'ARG2', 'ARG1_TEXT', 'ARG2_TEXT', 'GRAM_SIGNAL', 'TEXT_SIGNAL', 'TEXT']

    # @semanticbeeng @todo @jep
    # with outfile.openText(mode='w') as outstream:
    outstream = outfile.openText('w')
    for out in output:

        if out['CLASS'] == 'RELATION':
            if 'SUBTYPE' in out:
                look_up = out['SUBTYPE']
            else:
                look_up = out['TYPE']

            ARG1_NAME: str = ARG1_NAME_TABLE[look_up]
            ARG2_NAME: str = ARG2_NAME_TABLE[look_up]

        fact: str = out['CLASS']
        for key in keys:
            if key in out:
                value = out[key]
                if type(value) == int:
                    value = str(value)
                else:
                    value = '"' + value + '"'

                fact = fact + ' ' + key + '=' + value

                if key == 'ARG1':
                    assert 'ARG1_NAME' in locals()
                    fact = fact + ' ARG1_NAME="' + ARG1_NAME + '"'
                elif key == 'ARG2':
                    assert 'ARG2_NAME' in locals()
                    fact = fact + ' ARG2_NAME="' + ARG2_NAME + '"'

        outstream.write(fact + os.linesep)


#
#
#
def bad_patent_line(line: str) -> bool:
    if (len(line) > 5000) and not (re.search('[a-z]', line)):
        return (True)
    else:
        return (False)


#
#   @semamanticbeeng @todo what is this doing?
#
def triplify(inlist: List[Dict[str, str]]) -> List[List[Dict[str, str]]]:
    if len(inlist) % 3 != 0:
        print('problem with triplify for:', inlist)
        return []     # [[{}]]       # @semanticbeeng @ todo static typing
    else:
        output = []
        start = 0
        while start < len(inlist):
            output.append(inlist[start:start + 3])
            start = start + 3
        return (output)


#
#  Find abbreviations for the content of a file fo @data TXT3
#
def run_abbreviate_on_lines(lines: List[str], abbr_file: File[ABBR], reset_dictionary: bool=False) -> List[Dict[str, str]]:

    # global abbr_to_full_dict
    # global full_to_abbr_dict
    global id_number

    output: List[Dict[str, str]] = []
    start = 0
    previous_line: str = None

    if reset_dictionary:
        Abbreviate.abbr_to_full_dict.clear()               # @semanticbeeng @todo @arch global state mutation
        Abbreviate.full_to_abbr_dict.clear()               # @semanticbeeng @todo @arch global state mutation
        id_number = 0

    # @semanticbeeng @todo not used with open(abbr_file, 'w') as outstream:
    abbr_file.openText('w')     # create even empty

    for line in lines:
        line = line.replace(os.linesep, ' ')
        end: int = start + len(line)
        trimmed_line = line.strip(' \t')
        out: List[Dict[str, str]] = []

        if ((trimmed_line.count('\t') + trimmed_line.count(' ')) > (len(trimmed_line) / 3)) or bad_patent_line(trimmed_line):
            pass

        else:
            out = get_next_abbreviate_relations(previous_line, line, start)

            if out:
                for triple in triplify(out):
                    if triple[1]['CLASS'] == 'ENAMEX':
                        argtype = triple[1]['TYPE']
                    else:
                        argtype = triple[1]['CLASS']
                    if argtype == 'JARGON':
                        record_abbreviate_dictionary(triple[0]['TEXT'], triple[1]['TEXT'])
                output.extend(out)
        start = end
        previous_line = line

    # @semanticbeeng @todo @arch global state control - this fails
    # abbr_to_full_dict = dictionary.freeze_dict(abbr_to_full_dict)
    # full_to_abbr_dict = dictionary.freeze_dict(full_to_abbr_dict)

    if output:
        #   @semanticbeeng @todo @dataFlow
        write_fact_file(output, abbr_file)

    return (output)


#
#
#
def save_abbrev_dicts(abbr_to_full_file: File[ABBR], full_to_abbr_file: File[ABBR]) -> None:

    with abbr_to_full_file.openText(mode='w') as abbr_full_stream, full_to_abbr_file.openText(mode='w') as full_abbr_stream:

        for key in Abbreviate.abbr_to_full_dict:
            abbr_full_stream.write(interior_white_space_trim(key))
            for value in Abbreviate.abbr_to_full_dict[key]:
                value = interior_white_space_trim(value)
                abbr_full_stream.write('\t' + value)
            abbr_full_stream.write(os.linesep)

        for key in Abbreviate.full_to_abbr_dict:
            full_abbr_stream.write(interior_white_space_trim(key))

            for value in Abbreviate.full_to_abbr_dict[key]:                # @semanticbeeng @todo @arch global state reference
                value = interior_white_space_trim(value)
                full_abbr_stream.write('\t' + value)

            full_abbr_stream.write(os.linesep)


#
#
#
def read_in_abbrev_dicts_from_files(abbr_to_full_file: File) -> None:       # @todo not used , full_to_abbr_file):
    # global abbr_to_full_dict
    # global full_to_abbr_dict

    Abbreviate.abbr_to_full_dict.clear()                                       # @semanticbeeng @todo @arch global state mutation
    Abbreviate.full_to_abbr_dict.clear()                                       # @semanticbeeng @todo @arch global state mutation

    with abbr_to_full_file.openText() as abbr_full_stream:          # @semanticbeeng @todo not used , open(full_to_abbr_file) as full_abbr_stream:

        for line in abbr_full_stream.readlines():
            line_list = line.strip().split('\t')
            Abbreviate.abbr_to_full_dict[line_list[0]] = line_list[1:]

        for line in Abbreviate.full_to_abbr_dict:                              # @semanticbeeng @todo how is this built?
            line_list = line.strip().split('\t')
            Abbreviate.full_to_abbr_dict[line_list[0]] = line_list[1:]         # @semanticbeeng @todo @arch global state mutation


#
#
#
def run_abbreviate_on_file_list(file_list: File, dict_prefix=False) -> None:
    start = True
    with file_list.openText() as instream:

        for line in instream.readlines():
            file_prefix: str = line.strip()

            # @semanticbeeng @todo @dataFlow
            lines: List[str] = get_lines_from_file(File[TXT3](file_prefix + '.txt3'))

            run_abbreviate_on_lines(lines, File[ABBR](file_prefix + '.abbr'), reset_dictionary=start)       # @semanticbeeng @todo @arch global state mutation

            if start:
                start = False

    if dict_prefix:
        save_abbrev_dicts(File[ABBR](str(dict_prefix) + ".dict_abbr_to_full"),
                          File[ABBR](str(dict_prefix) + ".dict_full_to_abbr"))


#
#
#
def get_expanded_forms_from_abbreviations(term: str) -> List[str]:
    variations = [term.upper(), term.lower()]
    if (len(variations[0]) > 2) and (variations[0][-1] == 'S'):
        variations.append(variations[0][:-1] + 's')
    output: List[str] = []
    ## print(variations)
    for variation in variations:
        if variation in Abbreviate.abbr_to_full_dict:
            for item in Abbreviate.abbr_to_full_dict[variation]:
                if not item in output:
                    ## print(2,'*',variation,'*',item)
                    output.append(item)
    return (output)


# #
# #   # @semanticbeeng dead code
# #
# def make_abbr_dicts_from_abbr(infiles: File, full_to_abbr_file: File[ABBR], abbr_to_full_file: File[ABBR]) -> None:
#     global abbr_to_full_dict
#     global full_to_abbr_dict
#
#     # @semanticbeeng @todo @arch global state mutation abbr_to_full_dict
#     abbr_to_full_dict.clear()
#     full_to_abbr_dict.clear()
#
#     arg1_pattern: Pattern[str] = re.compile('ARG1_TEXT="([^"]*)"')
#     arg2_pattern: Pattern[str] = re.compile('ARG2_TEXT="([^"]*)"')
#
#     with infiles.openText() as liststream:
#         for infile in liststream.readlines():
#             infile = infile.strip()
#
#             with File(infile).openText() as instream:
#                 for line in instream.readlines():
#                     if line.startswith('RELATION'):
#                         arg1_match = arg1_pattern.search(line)
#                         arg2_match = arg2_pattern.search(line)
#
#                         if arg1_match and arg2_match:
#                             full_name = arg1_match.group(1).upper()
#                             abbr = arg2_match.group(1).upper()
#
#                             # @semanticbeeng @todo @arch global state mutation abbr_to_full_dict
#                             if (abbr in abbr_to_full_dict):
#                                 if (not full_name in abbr_to_full_dict[abbr]):
#                                     abbr_to_full_dict[abbr].append(full_name)
#                             else:
#                                 abbr_to_full_dict[abbr] = [full_name]
#
#                             # @semanticbeeng @todo @arch global state mutation abbr_to_full_dict
#                             if (full_name in full_to_abbr_dict):
#                                 if (not abbr in full_to_abbr_dict[full_name]):
#                                     full_to_abbr_dict[full_name].append(abbr)
#                             else:
#                                 full_to_abbr_dict[full_name] = [abbr]
#
#     save_abbrev_dicts(abbr_to_full_file, full_to_abbr_file)
