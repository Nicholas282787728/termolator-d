#!/usr/bin/env python3

import os
import re
import sys
from DataDef import File

def main(args):
    ## infile is the output file from distributional term extraction
    txt_file_list = args[1]
    out_file = args[2]
    ## outfile is the main output dictionary file from this process
    extensions = args[3:]

    if extensions:
        with File(txt_file_list).openText() as instream, File(out_file).openText(mode='w') as outstream:
            for line in instream.readlines():
                line = line.strip()
                ending_pattern = re.compile('\.((txt)|(hml)|(htm)|(html)|(xml)|(sgml))[^a-zA-Z]*$', re.I)
                base = ending_pattern.sub('', line)
                if extensions[0] == 'BARE':
                    outstream.write(base)
                else:
                    outstream.write(base + extensions[0])
                for extension in extensions[1:]:
                    if extension.upper() in ['TRUE', 'FALSE', 'T', 'F']:
                        outstream.write(';' + extension)
                    elif extension.upper() == 'BARE':
                        outstream.write(base)
                    else:
                        outstream.write(';' + base + extension)
                outstream.write(os.linesep)


# @semanticbeeng @todo to run from Jep
if __name__ == '__main__': sys.exit(main(sys.argv))
