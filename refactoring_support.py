
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
def trace_args_and_return(frame, msg, arg):

    func_name: str = frame.f_code.co_name

    # TRACE = ['trace_OK_chemical']
    #
    # # Filter as appropriate
    # if func_name not in TRACE:
    #     return None

    print("tracing " + func_name)
    with open("trace_" + func_name + ".txt", mode='a') as out:
        if msg == 'call':
            out.write("(called   `{}`)".format(func_name) + "\n")
            for i in range(frame.f_code.co_argcount):
                name = frame.f_code.co_varnames[i]
                out.write("(    `{}` = {})".format(name, frame.f_locals[name]) + "\n")
            return trace_args_and_return
        elif msg == 'return':
            out.write("(returned `{}'`)".format(func_name) + "\n")
            out.write("(    `return` = {})".format(arg) + "\n")
            return None
        elif msg == 'line':
            return None
