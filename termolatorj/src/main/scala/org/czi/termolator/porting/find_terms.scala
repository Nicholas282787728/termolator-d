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
  def find_inline_terms_for_file_list(file_list : List[File[_]], dict_prefix : Option[String] = None) = {

    val functionName = "find_inline_terms_for_file_list"

    pyCall(functionName, File("DAVETEST.internal_prefix_list"), None) // @todo "dict_prefix=False")

    // @todo
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
