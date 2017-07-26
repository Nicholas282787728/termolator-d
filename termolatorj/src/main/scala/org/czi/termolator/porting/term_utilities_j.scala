package org.czi.termolator.porting

/**
  * Created by nickdsc on 7/12/17.
  */
object term_utilities_j {

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:1088]]
    */
  def get_my_string_list : List[String] = ???

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:1069]]
    */
  def merge_multiline_and_fix_xml(lines: List[String]) = ???

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:553]]
    */
  def remove_xml_spit_out_paragraph_start_end = ???

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:580]]
    */
  def replace_less_than_with_positions = ???

  /**
    * @code_reference [[./nyu-english-new/term_utilities.py:1002]]
    */
  def get_integrated_line_attribute_value_structure_no_list = {

    //@todo - no side effects
    null
  }

  import DataDef._
  /**
    * @code_reference [[term_utilities_j.get_lines_from_file]]
    */
  def get_lines_from_file(infile: File[_]) = ???
}
