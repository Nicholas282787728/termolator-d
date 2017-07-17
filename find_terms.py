from inline_terms import *
from DataDef import File, TXT3

#
#
#
def find_inline_terms_for_file_list(file_list: File, dict_prefix: bool = False) -> None:
    start = True
    with file_list.openText() as instream:
        # if dict_prefix:
        #     unigram_dictionary.clear()
        ## see derive_plurals in term_utilities
        ## and other instances of "unigram_dict" below
        for line in instream.readlines():
            file_prefix = line.strip()
            lines: List[str] = get_lines_from_file(File[TXT3](file_prefix + '.txt3'))  ## add feature to remove xml

            run_abbreviate_on_lines(lines, File[ABBR](file_prefix + '.abbr'), reset_dictionary=start)       # @semanticbeeng @todo @arch global state mutation
            ## creates abbreviation files and acquires abbreviation --> term
            ## and term --> abbreviation dictionaries
            ## Possibly add alternative which loads existing abbreviation files into
            ## dictionaries for future steps (depends on timing)

            # if dict_prefix:
            #     increment_unigram_dict_from_lines(lines)

            find_inline_terms(lines, file_prefix + '.fact', file_prefix + '.pos', file_prefix + '.terms')
            if start:
                start = False
        if dict_prefix:
            save_abbrev_dicts(File[ABBR](str(dict_prefix) + ".dict_abbr_to_full"),
                              File[ABBR](str(dict_prefix) + ".dict_full_to_abbr"))
            ## save_unigram_dict(dict_prefix+".dict_unigram")
