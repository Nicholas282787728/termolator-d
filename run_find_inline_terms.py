#!/usr/bin/env python3

from find_terms import *
from DataDef import File
import dictionary
from refactoring_support import Refactoring

def main(args):
    # global special_domains

    Refactoring.run_filter_phase = False

    file_list = args[1]
    if len(args) > 2:
        outfile_prefix = args[2]
    else:
        outfile_prefix = False
    if (len(args) > 3) and (args[3].lower() != 'false'):
        dictionary.special_domains.extend(args[3].split('+'))                                  # @semanticbeeng @todo @arch global state initialization

    dictionary.initialize_utilities()
    find_inline_terms_for_file_list(File(file_list), dict_prefix=outfile_prefix)


# @semanticbeeng @todo to run from @jep
if __name__ == '__main__': sys.exit(main(sys.argv))
