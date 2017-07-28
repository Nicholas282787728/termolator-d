import re
import dictionary
import term_utilities
from typing import List, Tuple, Dict, Pattern

#
#
#
class TermLemmer:

    class Patterns:
        compound_inbetween_string: Pattern[str] = re.compile('^ +(of|for) +((the|a|[A-Z]\.) +)?$', re.I)

    #
    #
    #
    def __init__(self, abbr_to_full_dict: Dict[str, List[str]]) -> None:

        self.lemma_dict: Dict[str, str] = {}
        self.lemma_count: Dict[str, int] = {}

        self.term_hash: Dict[str, List[Tuple[int, int]]] = {}
        self.term_type_hash: Dict[str, str] = {}
        self.head_hash: Dict[str, str] = {}

        # @semanticbeeng @global state : assert that this will not change from the time of construction
        self.abbr_to_full_dict = dictionary.freeze_dict(abbr_to_full_dict)

    #
    #
    #
    def process(self,
                term_tuples: List[Tuple[int, int, str, str]],
                big_txt: str):

        # compound_tuples = []              # @semanticbeeng @todo not used
        last_tuple: Tuple[int, int, str, str] = None        # @semanticbeeng @todo static typing  @data what is this

        # unit testing print("find_inline_terms >> ")
        for t_start, t_end, term, term_type in term_tuples:
            # unit testing
            # print("find_inline_terms >> tuple(" + str(t_start) + ", " + str(t_end) + ", " + term + ", " + term_type + ")")

            ## for now we will limit compounding not to function and
            ## lemmas not to merge entries unless term_type ==
            ## 'chunk-based'
            if term in self.term_hash:
                self.term_hash[term].append((t_start, t_end))                            # @semanticbeeng @todo static typing
                lemma = self.get_term_lemma(term, term_type=term_type)

                if lemma in self.lemma_count:
                    self.lemma_count[lemma] = self.lemma_count[lemma] + 1
                else:
                    self.lemma_count[lemma] = 1
            else:
                self.term_hash[term] = [(t_start, t_end)]                                # @semanticbeeng @todo static typing
                self.term_type_hash[term] = term_type

                lemma = self.get_term_lemma(term, term_type=term_type)

                if lemma in self.lemma_count:
                    self.lemma_count[lemma] = self.lemma_count[lemma] + 1
                else:
                    self.lemma_count[lemma] = 1

            if last_tuple and (t_start > last_tuple[1]) and (last_tuple[3] in [False, 'chunk-based']) and (term_type in [False, 'chunk-based']):
                inbetween = self.Patterns.compound_inbetween_string.search(big_txt[last_tuple[1]:t_start])

                if inbetween:
                    compound_term: str = term_utilities.interior_white_space_trim(big_txt[last_tuple[0]:t_end])
                    ## compound_term = re.sub('\s+',' ',big_txt[last_tuple[0]:t_end])

                    compound_tuple: Tuple[int, int, str, str] = (last_tuple[0], t_end, compound_term, 'chunk-based')        # @semanticbeeng @todo static typing @data ??
                    ## term_tuples.append(compound_tuple)

                    if compound_term in self.term_hash:
                        self.term_hash[compound_term].append((last_tuple[0], t_end))     # @semanticbeeng @todo static typing
                        lemma = self.get_compound_lemma(compound_term, last_tuple[2], term)

                        if lemma in self.lemma_count:
                            self.lemma_count[lemma] = self.lemma_count[lemma] + 1
                        else:
                            self.lemma_count[lemma] = 1
                    else:
                        self.term_hash[compound_term] = [(last_tuple[0], t_end)]           # @semanticbeeng @todo static typing
                        self.head_hash[compound_term] = last_tuple[2]
                        lemma = self.get_compound_lemma(compound_term, last_tuple[2], term)

                        if lemma in self.lemma_count:
                            self.lemma_count[lemma] = self.lemma_count[lemma] + 1
                        else:
                            self.lemma_count[lemma] = 1
                    last_tuple = compound_tuple[:]

                elif not re.search('[^\s]', big_txt[last_tuple[1]:t_start]):
                    compound_term = term_utilities.interior_white_space_trim(big_txt[last_tuple[0]:t_end])

                    compound_tuple = (last_tuple[0], t_end, compound_term, 'chunk-based')   #  @semanticbeeng @todo static typing

                    if compound_term in self.term_hash:
                        self.term_hash[compound_term].append((last_tuple[0], t_end))     #  @semanticbeeng @todo static typing
                        lemma = self.get_compound_lemma(compound_term, last_tuple[2], term)
                        if lemma in self.lemma_count:
                            self.lemma_count[lemma] = self.lemma_count[lemma] + 1
                        else:
                            self.lemma_count[lemma] = 1
                    else:
                        self.term_hash[compound_term] = [(last_tuple[0], t_end)]         #  @semanticbeeng @todo static typing
                        ## if there is only blank space and no
                        ## preposition between terms, the
                        ## compounding is normal noun noun
                        ## compounding, rather than the inversion
                        ## used for noun prep noun sequences
                        lemma = self.get_compound_lemma(compound_term, last_tuple[2], term)
                        self.head_hash[compound_term] = term
                        if lemma in self.lemma_count:
                            self.lemma_count[lemma] = self.lemma_count[lemma] + 1
                        else:
                            self.lemma_count[lemma] = 1
                else:
                    last_tuple = (t_start, t_end, term, term_type)      #  @semanticbeeng @todo static typing
            else:
                last_tuple = (t_start, t_end, term, term_type)          #  @semanticbeeng @todo static typing

    #
    #  @semanticbeeng @func comp_termChunker
    #  @semanticbeeng @todo static typing
    #
    def get_term_lemma(self, term: str, term_type: str=None) -> str:
        ## add plural --> singular
        ## print(term,term_type)
        # global lemma_dict

        last_word_pat = re.compile('[a-z]+$', re.I)

        if term in self.lemma_dict:
            return (self.lemma_dict[term])

        elif term_type and (term_type != 'chunk-based'):
            ## this takes care of all the patterned cases
            output = term.upper()

        elif (term in self.abbr_to_full_dict) and (len(self.abbr_to_full_dict[term]) > 0) and \
                (term.isupper() or (not term in dictionary.pos_dict) or (term in dictionary.jargon_words)):
            output = self.abbr_to_full_dict[term][0]

        else:
            last_word_match = last_word_pat.search(term)

            if last_word_match:
                last_word = last_word_match.group(0).lower()
                last_word_start = last_word_match.start()

                if (last_word in dictionary.noun_base_form_dict) and (not last_word.endswith('ing')):
                    if (last_word in dictionary.noun_base_form_dict[last_word]):
                        output = term.upper()
                    else:
                        output = (term[:last_word_start] + dictionary.noun_base_form_dict[last_word][0]).upper()
                elif last_word.endswith('ies'):
                    output = (term[:-3] + 'y').upper()
                elif last_word.endswith('es') and (len(last_word) > 3) and (last_word[-3] in 'oshzx'):
                    output = term[:-2].upper()
                elif last_word.endswith('(s)'):
                    output = term[:-3].upper()
                elif (len(last_word) > 1) and last_word.endswith('s') and term[-1].isalpha() and (not last_word[-2] in 'u'):
                    output = term[:-1].upper()
                else:
                    output = term.upper()
            elif re.search('\([sS]\)$', term):
                output = term[:-3].upper()
            else:
                output = term.upper()
        self.lemma_dict[term] = output           # @semanticbeeng @todo global state mutation
        return (output)


    #
    #
    #
    def get_compound_lemma(self, compound_term: str, first_term: str, second_term: str) -> str:
        if compound_term in self.lemma_dict:
            return (self.lemma_dict[compound_term])      # @semanticbeeng @todo global state reference
        else:
            first_lemma = self.get_term_lemma(first_term, term_type='chunk-based')
            second_lemma = self.get_term_lemma(second_term, term_type='chunk-based')
            output = (second_lemma + ' ' + first_lemma).upper()
            self.lemma_dict[compound_term] = output      # @semanticbeeng @todo global state mutation
            return (output)
