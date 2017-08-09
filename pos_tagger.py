import os
from typing import List, Dict
from DataDef import File, POS, POSTag


class POSTagger:

    #
    #
    #
    def __init__(self) -> None:
        self.pos_offset_table: Dict[int, str] = {}

    #
    #   @ssemanticbeeng @todo @global state pos_offset_table - clarify meaning since it may be empty if ran from filter_term_output.py
    #
    def get_tagger_pos(self, offset: int) -> POSTag:
        """
        Maps from Jet POS tags to `Termolator`:type:`POSTag`

        :param offset:
        :return:
        """
        if offset and (offset in self.pos_offset_table):
            tagger_pos = self.pos_offset_table[offset]  # @semanticbeeng @todo global state reference
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
    #   @semanticbeeng @todo consider moving this to dictionary.py
    #   @semanticbeeng @todo global state mutation or initialization ?
    #
    def load_pos_offset_table(self, pos_file: File[POS]) -> None:
        self.pos_offset_table.clear()

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
                self.pos_offset_table[start] = pos       # @semanticbeeng @data : is this PosTag

