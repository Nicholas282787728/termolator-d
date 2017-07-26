package org.czi.termolator.porting

/**
  *
  */
object find_terms extends JepEnabled {

  import DataDef._


  val moduleName = "find_terms"

  /**
    * @code_reference [[./nyu_english_new.find_terms.find_inline_terms_for_file_list]]
    */
  def find_inline_terms_for_file_list(file_list: File[File[BARE]], dict_prefix: Option[String] = None): Unit = {

    // @done ported FunctionDef("find_inline_terms_for_file_list", ("file_list", file_list), ("dict_prefix ", None)).pyCall()

    //    # if dict_prefix:
    //    #     unigram_dictionary.clear()
    //    ## see derive_plurals in term_utilities
    //    ## and other instances of "unigram_dict" below
    var start = true
    file_list.readlines() foreach { f ⇒

      val file_prefix = f.trim

      val lines: List[String] = term_utilities.get_lines_from_file(File[TXT3](file_prefix + ".txt3"))

      abbreviate.run_abbreviate_on_lines(lines, File[ABBR](file_prefix + ".abbr"), reset_dictionary = start)

      //      ## creates abbreviation files and acquires abbreviation --> term
      //      ## and term --> abbreviation dictionaries
      //      ## Possibly add alternative which loads existing abbreviation files into
      //      ## dictionaries for future steps (depends on timing)
      //
      //      # if dict_prefix:
      //      #     increment_unigram_dict_from_lines(lines)
      //
      inline_terms.find_inline_terms(lines, File[FACT](file_prefix + ".fact"), File[POS](file_prefix + ".pos"),
        File[TERMS](file_prefix + ".terms"))

      start = false
    }

    if (dict_prefix.isDefined)
      abbreviate.save_abbrev_dicts(File[ABBR](dict_prefix.get + ".dict_abbr_to_full"), File[ABBR](dict_prefix.get + ".dict_full_to_abbr"))
    // save_unigram_dict(dict_prefix+".dict_unigram")
  }
}
