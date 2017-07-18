#!/usr/bin/env python3
import sys

from abbreviate import *
from DataDef import File
import dictionary

def main(args):
    # global special_domains
    file_list = args[1]
    if len(args) > 2:
        outfile_prefix = args[2]
    else:
        outfile_prefix = False
    if (len(args) > 3) and (args[3].lower() != 'false'):
        dictionary.special_domains.extend(args[3].split('+'))                                  # @semanticbeeng @todo @arch global state initialization

    dictionary.initialize_utilities()
    run_abbreviate_on_file_list(File(file_list), dict_prefix=outfile_prefix)        # @semanticbeeng @todo @arch global state mutation


if __name__ == '__main__': sys.exit(main(sys.argv))
