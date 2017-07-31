
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
#
def trace_args_and_return(frame, msg, arg):
    if msg == 'call':
        # Filter as appropriate
        if frame.f_code.co_filename.startswith("/development/bin"):
            return
        print("called   `", frame.f_code.co_name, '`')
        for i in range(frame.f_code.co_argcount):
            name = frame.f_code.co_varnames[i]
            print("    `", name, "`=", frame.f_locals[name])
        return trace_args_and_return
    elif msg == 'return':
        print("returned `", frame.f_code.co_name, '`')
        print("    `", 'return', "`=", arg)
        return None
    elif msg == 'line':
        return None
