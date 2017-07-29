#!/usr/bin/env python3

from filter_terms import *
from DataDef import File, TERM, ABBR
import dictionary
from refactoring_support import Debug

def main(args):
    # global special_domains

    Debug.run_without_pos = True

    file_prefix = args[1]
    web_score_dict_file = args[2]
    if args[3].lower() in ['true', 't']:
        use_web_score = True
    elif args[3].lower() in ['false', 'f']:
        use_web_score = False
    else:
        print('You set the webscore flag to', args[2], 'but it must be either "True" or "False".')
        print('Use "True" if you want the system to use the webscore function and the system will run slowly and be more accurate.')
        print('Use "False" otherwise.')

    max_term_number = int(args[4])

    if (len(args) > 5) and (args[5].lower() != 'false'):
        dictionary.special_domains.extend(args[5].split('+'))              # @semanticbeeng @todo @arch global state initialization

    dictionary.initialize_utilities()

    input_file = File[TERM](file_prefix + ".all_terms")
    output_file = File(file_prefix + ".scored_output")
    abbr_full_file = File[ABBR](file_prefix + ".dict_abbr_to_full")
    # @semanticbeeng @todo not used  full_abbr_file = file_prefix + ".dict_full_to_abbr"
    reject_file = File(file_prefix + ".rejected-terms")

    filter_terms(input_file, output_file, abbr_full_file,
                 # @semanticbeeng @todo not used  full_abbr_file,
                 use_web_score,
                 numeric_cutoff=max_term_number,
                 reject_file=reject_file,
                 web_score_dict_file=File(web_score_dict_file))


if __name__ == '__main__': sys.exit(main(sys.argv))
