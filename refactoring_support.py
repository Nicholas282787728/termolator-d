from typing import Dict, List
import json

#
# Misc things to support the effort to comprehend, de-entangle and refactor the code
#
class Refactoring:

    run_filter_phase: bool = None

    # @todo @tdata : are TXT2 and TXT3 files ever different than TXT? are they every written to after creation?
    datadef_TXT_files: bool


#
# System trace to dump arguments and returns for purpose of program comprehension and test generation
# @resource https://pymotw.com/2/sys/tracing.html
# @resource https://docs.python.org/3.0/library/trace.html
#

CallInfo = Dict[str, Dict[str, str]]
calls: Dict[str, List[CallInfo]] = {}
# callPos: Dict[str, int] = {}

def trace_args_and_return(frame, msg, arg):

    func_name: str = frame.f_code.co_name

    TRACE = ['get_topic_terms',
             'get_formulaic_term_pieces',
             'merge_formulaic_and_regular_term_tuples',
             'topic_term_ok',
             'guess_pos',
             'get_next_word',
             'interior_white_space_trim',
             'topic_term_ok_boolean',
             'get_term_lemma',
             'get_compound_lemma',
             'nom_class']

    # Filter as appropriate
    if func_name not in TRACE:
        return None

    print("tracing " + func_name)
    with open("trace_" + func_name + ".json", mode='a') as out:
        if msg == 'call':

            paramInfo: Dict[str, str] = {}
            thisCall : CallInfo = {
                "funcName": func_name,
                "args": paramInfo
            }

            # out.write("called   `{}`".format(func_name) + "\n")

            for i in range(frame.f_code.co_argcount):
                name = frame.f_code.co_varnames[i]
                paramInfo[name] = str(frame.f_locals[name])
                # out.write("    `{}` = {}".format(name, str(frame.f_locals[name])) + "\n")

            # print(json.dumps(thisCall))
            # out.write(json.dumps(thisCall))

            funcCalls: List[CallInfo] = []
            if func_name in calls:
                funcCalls = calls[func_name]

            funcCalls.append(thisCall)
            calls[func_name] = funcCalls

            return trace_args_and_return

        elif msg == 'return':

            funcCalls: List[CallInfo] = calls[func_name]
            if not funcCalls:
                assert False, "No calls for " + func_name

            # thisCallPos: int = callPos[func_name]
            thisCall: CallInfo = funcCalls.pop()
            thisCall["return"] = arg
            # callPos[func_name] = thisCallPos - 1

            # out.write("returned `{}`".format(func_name) + "\n")
            # out.write("    `return` = {}".format(arg) + "\n")
            out.write(json.dumps(thisCall) + ",\n")
            return None

        elif msg == 'line':
            return None
