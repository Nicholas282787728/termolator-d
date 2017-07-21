#!/usr/bin/env python3

import os
import re
import sys
from typing import List, Tuple, Optional, Pattern, Match
from DataDef import File, ABBR, POS, PosFact

#
#
#
def get_pos_facts(fact_list: List[ABBR]) -> List[PosFact]:
    output: List[PosFact] = []
    bad_pos_pattern: Pattern[str] = re.compile('BAD_CHARACTER START=([0-9]*) END=([0-9]*) STRING="([^"]*)"')

    for fact in fact_list:
        bad_match: Optional[Match[str]] = bad_pos_pattern.search(fact)
        if bad_match:
            output.append(PosFact(int(bad_match.group(1)), int(bad_match.group(2)), bad_match.group(3)))   # @semanticbeeng @todo static typing
    return (output)


#
#
#
def make_fact_pair(triple: PosFact) -> Tuple[int, str]:
    output = (triple[0], triple[2] + ' ||| S:' + str(triple[0]) + ' E:' + str(triple[1]) + ' ||| ' + 'SYM' + os.linesep)  # @semanticbeeng @todo static typing
    return (output)


#
#
#
def make_pos_triple(line: str) -> PosFact:
    start_pat = re.compile('S:([0-9]*).*E:([0-9]*)')
    start_match = start_pat.search(line)
    if not start_match:
        print('Warning: Error in POS file')
        return (PosFact(0, 0, line))       # @semanticbeeng @todo static typing @data PosFact
    else:
        return (PosFact(int(start_match.group(1)), int(start_match.group(2)), line))   # @semanticbeeng @todo static typing @data PosFact


#
#
#
def modify_pos_end(line: str, new_end: int) -> str:
    start_pat = re.compile('E:([0-9]*)')
    start_match = start_pat.search(line)
    if start_match:
        output = line[0:start_match.start()] + 'E:' + str(new_end) + line[start_match.end():]
        return (output)
    else:
        return (line)


#
#
#
def fix_bad_char_in_file(fact: File[ABBR], pos: File[POS]):

    with fact.openText() as fact_stream:
        fact_list: List[PosFact] = get_pos_facts(fact_stream.readlines())
        fact_list.reverse()

    if fact_list:
        with pos.openText() as pos_stream:
            pos_list: List[str] = pos_stream.readlines()
            pos_list.reverse()

        next_fact: Tuple[int, str] = None        # @semanticbeeng @todo static typing
        next_pos: PosFact = None                 # @semanticbeeng @todo static typing

        with pos.openText(mode='w') as outstream:
            while pos_list or fact_list:
                if fact_list and (not next_fact):
                    next_fact = make_fact_pair(fact_list.pop())
                if pos_list and (not next_pos):
                    next_pos = make_pos_triple(pos_list.pop())
                if (next_pos and next_fact and (next_pos[0] > next_fact[0])) or (next_fact and not next_pos):
                    outstream.write(next_fact[1])
                    next_fact = None       # @semanticbeeng @todo static typing
                elif next_pos:
                    if next_fact and (next_fact[0] > next_pos[0]) and (next_fact[0] < next_pos[1]):
                        outstream.write(modify_pos_end(next_pos[2], next_fact[0]))
                    else:
                        outstream.write(next_pos[2])
                    next_pos = None        # @semanticbeeng @todo static typing


def main(args):
    file_list = args[1]
    lines = []
    with File(file_list).openText() as instream:
        for line in instream.readlines():
            fact, pos = line.strip().split(';')
            fix_bad_char_in_file(File[ABBR](fact), File[POS](pos))


if __name__ == '__main__': sys.exit(main(sys.argv))
