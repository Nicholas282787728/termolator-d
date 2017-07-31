package org.czi.termolator.porting

/**
  *
  */
object term_utilities extends JepEnabled {

  import DataDef._


  val moduleName = "term_utilities"

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:1088]]
    */
  def get_my_string_list: List[str] = List.empty

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:1069]]
    */
  def merge_multiline_and_fix_xml(lines: List[str]) = List.empty

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:553]]
    */
  def remove_xml_spit_out_paragraph_start_end = Unit

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:580]]
    */
  def replace_less_than_with_positions = Unit

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:1002]]
    */
  def get_integrated_line_attribute_value_structure_no_list = {

    //@todo - no side effects
    null
  }

  import DataDef._


  /**
    * @code_reference [[term_utilities.get_lines_from_file]]
    */
  def get_lines_from_file(infile: File[_]): List[str] = {
    import collection.JavaConverters._
    FunctionDef("get_lines_from_file", ("infile", infile)).pyCallAndReturn[java.util.List[str]]().asScala.toList
  }

  /**
    *
    */
  def nom_class(word: str, pos: str): int = {
    FunctionDef("nom_class", ("word", word), ("pos", pos)).pyCallAndReturn[jep.int]().toLong
  }
}
