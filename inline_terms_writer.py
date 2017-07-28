import re, os
import term_utilities
import dictionary
from typing import List, Tuple, Dict, Optional, Pattern

import inline_terms_lemmer      # @todo remove this dependency

#
#   Perists the TERMSS for a single source "file"
#
class TermsWriter:

    class Patterns:
        et_al_citation: Pattern[str] = re.compile(' et[.]? al[.]? *$')

    def __init__(self, outstream) -> None:
        self.outstream = outstream
        self.term_id_number = 0

    #
    # @semanticbeeng @dataFlow
    #
    def write_all(self, term_list: List[str],
                  lemmer: inline_terms_lemmer.TermsLemmer):

        # @semanticbeeng @global state : ensure no mutations from here on
        term_hash: Dict[str, List[Tuple[int, int]]] = lemmer.term_hash
        term_type_hash: Dict[str, str] = dictionary.freeze_dict(lemmer.term_type_hash)
        head_hash: Dict[str, str] = dictionary.freeze_dict(lemmer.head_hash)
        lemma_dict : Dict[str, str] = dictionary.freeze_dict(lemmer.lemma_dict)
        lemma_count: Dict[str, int] = dictionary.freeze_dict(lemmer.lemma_count)

        for term in term_list:

            if (term in term_type_hash) and (not term_type_hash[term] in [False, 'chunk-based']):
                self.write_term_summary_fact_set(term, term_hash[term],
                                                       lemma_dict, lemma_count,
                                                       head_term=term.upper(), head_lemma=term.upper(), term_type=term_type_hash[term])

            elif self.Patterns.et_al_citation.search(term):
                self.write_term_becomes_article_citation(term, term_hash[term])

            elif term_utilities.org_ending_pattern.search(term) or self.org_head_ending(term, head_hash):
                self.write_term_becomes_organization(term, term_hash[term])

            elif term_utilities.person_ending_pattern.search(term):
                self.write_term_becomes_person(term, term_hash[term])

            elif self.term_is_org_with_write(term, term_hash[term]):
                pass
            else:
                if term in head_hash:
                    head_term: str = head_hash[term]

                    if head_term in lemma_dict:
                        head_lemma = lemma_dict[head_term]
                    elif head_term in term_type_hash:
                        head_lemma = lemmer.get_term_lemma(head_term, term_type=(term_type_hash[head_term]))
                    else:
                        head_lemma = lemmer.get_term_lemma(head_term)
                else:
                    head_term = None           #  @semanticbeeng @todo static typing
                    head_lemma = None              #  @semanticbeeng @todo static typing
                #   @semanticbeeng @todo @dataFlow

                self.write_term_summary_fact_set(term, term_hash[term], lemma_dict, lemma_count,
                                                       head_term=head_term, head_lemma=head_lemma)

    #
    #   @semanticbeeng @todo
    #
    def term_is_org_with_write(self, term: str, instances: List[Tuple[int, int]]) -> bool:

        if not re.search('[A-Z]', term[0]):
            return (False)

        words = term_utilities.divide_sentence_into_words_and_start_positions(term)
        person_names = 0
        Fail = False
        ambiguous_person_names = 0
        word_pattern = []
        if re.search('^[A-Z][a-z]', words[-1][1]):
            if term_utilities.last_word_organization.search(words[-1][1]):
                ends_in = 'ORG'
            elif term_utilities.last_word_gpe.search(words[-1][1]):
                ends_in = 'GPE'
            elif term_utilities.last_word_loc.search(words[-1][1]):
                ends_in = 'LOC'
            else:
                ends_in = None              # @semanticbeeng @todo static typing
        else:
            ends_in = None                  # @semanticbeeng @todo static typing
    
        for position, word in words:
            lower = word.lower()
            is_capital = re.search('^[A-Z][a-z]', word)
    
            if is_capital and (lower in dictionary.pos_dict) and ('PERSON_NAME' in dictionary.pos_dict[lower]):
                person_names = person_names + 1
                if len(dictionary.pos_dict[lower]) > 1:
                    ambiguous_person_names = ambiguous_person_names + 1
                    word_pattern.append('ambig_name')
                else:
                    word_pattern.append('name')
            else:
                word_pattern.append('not_name')
    
            if is_capital or term_utilities.closed_class_check2.search(word):
                pass
            else:
                Fail = True
    
        if not term_utilities.ambig_last_word_org.search(words[-1][1]):
            length_name_criterion = True
        elif (len(words) < 4) or \
                ((person_names > 1) and (person_names > ambiguous_person_names)):
            length_name_criterion = True
        else:
            length_name_criterion = False
    
        if (len(words) <= 1) or (not ' ' in term):
            return (False)
        elif (ends_in == 'ORG') and length_name_criterion:
            ne_class = 'ORGANIZATION'
        elif (ends_in == 'GPE') and length_name_criterion:
            ne_class = 'GPE'
        elif (ends_in == 'LOC') and length_name_criterion:
            ne_class = 'LOCATION'
        elif person_names == 0:
            return (False)
        elif (len(words) == 2) and (person_names == 2) and (person_names > ambiguous_person_names) and (' ' in term) \
                and (word_pattern[-1] == 'name'):
            ## all words of an organization except for closed class words should
            ## be capitalized.
            ## However, 2 word capitalized phrases can be person names, particularly if
            ## both words are in our person dictionary, so let's not include these
            ## If first word is a name and second word is a non-name, probably this is not
            ## an organization.
            ne_class = 'ORGANIZATION_OR_GPE'
        elif Fail:
            return (False)
        else:
            ## ne_class = 'ORGANIZATION'
            return (False)
        # global term_id_number @semanticbeeng @global state
    
        for start, end in instances:
            self.term_id_number = 1 + self.term_id_number
            self.outstream.write(ne_class + ' ID="NYU_ID_' + str(self.term_id_number) + '" STRING="' + term + '"')
            self.outstream.write(' START=' + str(start) + ' END=' + str(end) + os.linesep)
        return (True)

    #
    #   @semanticbeeng @todo static type
    #
    def write_term_summary_fact_set(self, term: str, instances: List[Tuple[int, int]],
                                    lemma_dict: Dict[str, str], lemma_count: Dict[str, int],
                                    head_term: Optional[str]=None, head_lemma: Optional[str]=None, term_type: Optional[str]=None) -> None:
        # global term_id_number @semanticbeeng global state
        frequency = len(instances)
        lemma = lemma_dict[term]
        lemma_freq = lemma_count[lemma]
    
        for start, end in instances:
            self.term_id_number = 1 + self.term_id_number
            if term_type == 'url':
                self.outstream.write('URL ID="NYU_TERM_' + str(self.term_id_number) + '" STRING="' + self.term_string_edit(term) + '"' + ' FREQUENCY=' + str(frequency))
            else:
                self.outstream.write('TERM ID="NYU_TERM_' + str(self.term_id_number) + '" STRING="' + self.term_string_edit(term) + '"' + ' FREQUENCY=' + str(frequency))
            self.outstream.write(' START=' + str(start) + ' END=' + str(end))
            self.outstream.write(' LEMMA="' + self.term_string_edit(lemma) + '" LEMMA_FREQUENCY=' + str(lemma_freq))
            if head_term:
                self.outstream.write(' HEAD_TERM="' + self.term_string_edit(head_term) + '"')
            if head_lemma:
                self.outstream.write(' HEAD_LEMMA="' + self.term_string_edit(head_lemma) + '"')
            if term_type and (not term_type == 'url'):
                self.outstream.write(' TERM_PATTERN_TYPE="' + term_type + '"')
            self.outstream.write(os.linesep)
    
    #
    #
    #
    def write_term_becomes_article_citation(self, term: str, instances: List[Tuple[int, int]]) -> None:
        # global term_id_number @semanticbeeng @global state
        for start, end in instances:
            self.term_id_number = 1 + self.term_id_number
            self.outstream.write('CITATION ID="NYU_ID_' + str(self.term_id_number) + '" STRING="' + term + '" CITE_CLASS="article"')
            self.outstream.write(' START=' + str(start) + ' END=' + str(end) + os.linesep)
    
    #
    #
    #
    def write_term_becomes_organization(self, term: str, instances: List[Tuple[int, int]]) -> None:
        # global term_id_number @semanticbeeng @global state
        for start, end in instances:
            self.term_id_number = 1 + self.term_id_number
            self.outstream.write('ORGANIZATION ID="NYU_ID_' + str(self.term_id_number) + '" STRING="' + term + '"')
            self.outstream.write(' START=' + str(start) + ' END=' + str(end) + os.linesep)
    
    #
    #
    #
    def write_term_becomes_gpe(self, term: str, instances: List[Tuple[int, int]]) -> None:
        # global term_id_number @semanticbeeng @global state
        for start, end in instances:
            self.term_id_number = 1 + self.term_id_number
            self.outstream.write('GPE ID="NYU_ID_' + str(self.term_id_number) + '" STRING="' + term + '"')
            self.outstream.write(' START=' + str(start) + ' END=' + str(end) + os.linesep)
    
    #
    #
    #
    def write_term_becomes_person(self, term: str, instances: List[Tuple[int, int]]) -> None:
        # global term_id_number @semanticbeeng @global state
        for start, end in instances:
            self.term_id_number = 1 + self.term_id_number
            self.outstream.write('PERSON ID="NYU_ID_' + str(self.term_id_number) + '" STRING="' + term + '"')
            self.outstream.write(' START=' + str(start) + ' END=' + str(end) + os.linesep)

    #
    #
    #
    @staticmethod
    def term_string_edit(instring: str) -> str:
        output = re.sub('>', '&gt;', instring)
        return (output)

    #
    #
    #
    @staticmethod
    def org_head_ending(term: str, head_hash) -> bool:
        if (term in head_hash) and term_utilities.org_ending_pattern.search(head_hash[term]):
            return (True)
        return (False)
