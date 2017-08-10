#!/usr/bin/env python3

import sys

from term_utilities import *
import dictionary
from typing import List
from DataDef import File, TXT, TXT2, TXT3, ABBR, FACT

dictionary.initialize_utilities()

#
#
#
def modify_paragraph_delimiters(paragraph_starts: List[int], paragraph_ends: List[int], paragraph_non_starts: List[int], paragraph_non_ends: List[int]):
    matched_outstarts: List[int] = []
    matched_outends: List[int] = []
    # next_start = 'Empty'      # @semanticbeeng @todo static typing

    while (len(paragraph_starts) > 0):
        next_start = paragraph_starts.pop(0)
        matched_outstarts.append(next_start)
        if (len(paragraph_ends) > 0):
            if (len(paragraph_starts) > 0) and (paragraph_starts[0] < paragraph_ends[0]):
                matched_outends.append(paragraph_starts[0])
            else:
                matched_outends.append(paragraph_ends.pop(0))
        elif len(paragraph_starts) > 0:
            matched_outends.append(paragraph_starts[0])
    paragraph_starts = matched_outstarts
    paragraph_ends = matched_outends
    out_starts: List[int] = []
    out_ends: List[int] = []
    current_start, current_end, current_non_start, current_non_end = None, None, None, None
    ## First step, use paragraph starts and ends to block unprintable sections (as per paragraph_non_starts,paragraph_non_ends)
    ## None means no value -- cannot use 0 because 0 is a possible file position; cannot use False, because False == 0 in Python
    if ((paragraph_non_ends) == 0) or (len(paragraph_non_starts) == 0):
        out_starts = paragraph_starts
        out_ends = paragraph_ends
    else:
        while (len(paragraph_ends) > 0) or (current_end is not None):
            if (current_start is None) and (len(paragraph_starts) > 0):
                current_start = paragraph_starts.pop(0)
            if (current_end is None):
                current_end = paragraph_ends.pop(0)
            if (current_non_start is None) and (len(paragraph_non_starts) > 0):
                current_non_start = paragraph_non_starts.pop(0)
            if (current_non_end is None) and (len(paragraph_non_ends) > 0):
                current_non_end = paragraph_non_ends.pop(0)
            if (current_non_start is not None) and (current_non_start <= current_start) and (current_non_end >= current_end):
                current_non_start = current_end
                current_start = None
                current_end = None
            if (current_non_end is not None) and (current_start is not None) and (current_non_end <= current_start):
                current_non_start = None
                current_non_end = None
            if (current_non_start is not None) and (current_start is not None) and (current_non_end is not None) and (current_non_start <= current_start) \
                    and (current_non_end >= current_start) and (current_non_end <= current_end):
                current_non_start = current_start
            if (current_start is None):
                pass
            elif (current_non_start is None) or ((current_end is not None) and (current_non_start >= current_end)) or \
                    ((current_non_end is not None) and (current_non_end <= current_start)):
                if current_start is not None:
                    out_starts.append(current_start)
                out_ends.append(current_end)
                current_start = None
                current_end = None
            elif (current_non_start is not None) and (current_non_end is not None) and (current_non_start <= current_start) and (current_end is not None) and (
                current_non_end >= current_end):
                current_start = None
                current_end = None
            elif (current_end is not None) and (current_non_start <= current_end) and (current_non_start >= current_start):
                out_starts.append(current_start)
                out_ends.append(current_non_start)
                last_start = current_start
                current_start = None
                current_non_start = None
                if (current_non_end is not None) and (current_non_end <= current_end):
                    if current_non_end >= last_start:
                        current_start = current_non_end
                    current_non_end = None
                elif (len(paragraph_starts) > 0) and (current_non_end is not None) and (paragraph_starts[0] <= current_non_end):
                    current_end = None
                    num = 0
                    while (num < len(paragraph_starts)) and (paragraph_starts[num] <= current_non_end):
                        paragraph_starts[num] = current_non_end
                        num = 1 + num
                    num = 0
                    while (num < len(paragraph_ends)) and (paragraph_ends[num] <= current_non_end):
                        paragraph_ends[num] = current_non_end
                        num = 1 + num
                    current_end = None
                    current_non_end = None
                else:
                    current_end = None
                    current_non_end = None
            elif (current_non_end >= current_start) and (current_end is not None) and (current_non_end <= current_end):
                current_start = current_non_end
                current_non_end = None
                current_non_start = None
    return (out_starts, out_ends)


#
#
#
def create_termolotator_fact_txt_files(input_file: File[TXT], txt2_file: File[TXT2], txt3_file: File[TXT3], fact_file: File[FACT]) -> None:
    # global paragraph_starts   # @semanticbeeng @todo not used
    # global paragraph_ends     # @semanticbeeng @todo not used

    paragraph_starts: List[int] = [0]      # @semanticbeeng @todo @dataflow
    paragraph_ends: List[int] = []         # @semanticbeeng @todo @dataflow
    nonprint_starts: List[int] = []
    nonprint_ends: List[int] = []
    bad_chars = []
    inlinelist = get_my_string_list(input_file)

    # @semanticbeeng @todo @jep
    # with txt2_file.openText(mode='w') as txt2_stream, txt3_file.openText(mode='w') as txt3_stream:

    txt2_stream = txt2_file.openText('w')
    txt3_stream = txt3_file.openText('w')
    start = 0
    length = 0

    for line in merge_multiline_and_fix_xml(inlinelist):
        string2, starts1, ends1, nonprint_starts1, nonprint_ends1 = remove_xml_spit_out_paragraph_start_end(line, start)
        string3, bad1 = replace_less_than_with_positions(string2, start)

        # # @semanticbeeng @todo debug
        if type(bad1) != list:
            print("ERROR ++++++ " + string3 + " , " + str(bad1))
            raise ValueError("Unexpected type for " + str(bad1))

        if (len(paragraph_ends) == 0) and (len(starts1) > 0) and (len(paragraph_ends) == 0):
            hypothetical_end = (starts1[0] - 1)
            if not hypothetical_end in ends1:
                ends1.append(hypothetical_end)
                ends1.sort()
                ## balances the addition of 0 as a start

        length = length + len(string2)
        start = start + len(string2)

        #
        #   @semanticbeeng @todo @dataflow - writing to both TXT2 and TXT3 files
        #
        txt2_stream.write(string2)
        txt3_stream.write(string3)

        paragraph_starts.extend(starts1)
        paragraph_ends.extend(ends1)
        nonprint_starts.extend(nonprint_starts1)
        nonprint_ends.extend(nonprint_ends1)
        bad_chars.extend(bad1)
    if len(paragraph_ends) > 0:
        paragraph_starts.append(1 + paragraph_ends[-1])
    paragraph_ends.append(length)

    paragraph_starts, paragraph_ends = modify_paragraph_delimiters(paragraph_starts, paragraph_ends, nonprint_starts, nonprint_ends)

    # @semanticbeeng @todo @jep
    # with fact_file.openText(mode='w') as factstream:
    factstream = fact_file.openText('w')

    if len(paragraph_starts) == len(paragraph_ends):
        for item_num in range(len(paragraph_starts)):
            factstream.write('STRUCTURE TYPE="TEXT" START=' + str(paragraph_starts[item_num]) + ' END=' + str(paragraph_ends[item_num]) + os.linesep)

    elif (len(paragraph_starts) > 1) and len(paragraph_ends) == 1:
        last_start = 0

        #
        #   @semanticbeeng @todo @dataflow - writing FACT files
        #
        for start in paragraph_starts:
            if start != 0:
                factstream.write('STRUCTURE TYPE="TEXT" START=' + str(last_start) + ' END=' + str(start) + os.linesep)
            last_start = start
        factstream.write('STRUCTURE TYPE="TEXT" START=' + str(last_start) + ' END=' + str(paragraph_ends[0]) + os.linesep)
    else:
        factstream.write('STRUCTURE TYPE="TEXT" START=0 END=' + str(paragraph_ends[0]) + os.linesep)

    #
    #   @semanticbeeng @todo @dataflow - writing FACT files
    #
    for bad_char in bad_chars:
        factstream.write('BAD_CHARACTER START=' + str(bad_char[0]) + ' END=' + str(bad_char[1]) + ' STRING="<"' + os.linesep)


def main(args):
    ## infile is the output file from distributional term extraction
    txt_file_list = args[1]
    file_type = args[2]
    if not file_type.lower() in ['.htm', '.html', '.txt', '.hml', '.xml', '.xhtml', '.sgm', '.sgml', '.xhml']:
        print('Warning: File type must be a member of the list', ['.htm', '.html', '.txt', '.hml', '.xml', '.xhtml', '.sgm', '.sgml', '.xhml'])
        print('Halting Program. Choose a member of this list and run this function again.')
        return ('Fail')
    with File(txt_file_list).openText() as instream:
        for line in instream.readlines():
            infile = line.strip()
            input_file = File(infile + file_type)
            txt2_file = File[TXT2](infile + '.txt2')
            txt3_file = File[TXT3](infile + '.txt3')
            fact_file = File[ABBR](infile + '.fact')        # @semanticbeeng @todo static typing: is FACT same as ABBR?
            create_termolotator_fact_txt_files(input_file, txt2_file, txt3_file, fact_file)


# @semanticbeeng @todo to run from @jep
if __name__ == '__main__': sys.exit(main(sys.argv))
