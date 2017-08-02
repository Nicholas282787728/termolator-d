package org.czi.termolator.porting

/**
  *
  */
object term_utilities extends JepEnabled {

  import DataDef._


  val moduleName = "term_utilities"

  /**
    *
    */
  val org_ending_pattern : Pattern = re.compile("([A-Z0-9_]+) *[=] *(([\"][^\"]*[\"])|([0-9]+))", re.I)
  val person_ending_pattern: Pattern = null
  val last_word_organization: Pattern = null
  val last_word_gpe : Pattern = null
  val last_word_loc: Pattern = null
  val closed_class_check2: Pattern = null
  val ambig_last_word_org: Pattern = null


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

  /**
    *
    */
  def divide_sentence_into_words_and_start_positions(sentence: str, start: int = 0) : List[Tuple[int, str]] = {
    null
  }

  /**
    *
    */
  def interior_white_space_trim(instring: str) : str = {
      val out1 = re.sub("\s+", " ", instring)
      val out2 = re.sub("\s*(.*[^\s])\s*$", "\g<1>", out1)
      return (out2)
  }

}
