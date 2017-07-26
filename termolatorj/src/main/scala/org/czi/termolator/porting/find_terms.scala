package org.czi.termolator.porting

/**
  *
  */
object find_terms extends JepEnabled {

  import DataDef_j._

  val moduleName = "find_terms.py"

  /**
    * @code_reference [[./nyu_english_new.find_terms.find_inline_terms_for_file_list]]
    */
  def find_inline_terms_for_file_list(file_list : List[File[_]], dict_prefix : Boolean = false) = {

    val functionName = "find_inline_terms_for_file_list"

    jep.eval("dictionary.initialize_utilities()")
    //jep.eval("find_inline_terms_for_file_list(File('DAVETEST.internal_prefix_list'), dict_prefix=False)")

    call(functionName, "File('DAVETEST.internal_prefix_list')", "dict_prefix=False")

//    file_list map { file : File[_] ⇒
//      term_utilities.get_lines_from_file(file)
//
//      abbreviate.run_abbreviate_on_lines(null, null, false) //@todo
//
//      inline_terms.find_inline_terms(lines = null,
//        fact_file = null,
//        pos_file = null,
//        terms_file= null,
//        marked_paragraphs = false,
//        filter_off = false)
//
//      val fileAbbr = _
//      abbreviate.save_abbrev_dicts(fileAbbr, null) //@todo
//    }
    null
  }
}
