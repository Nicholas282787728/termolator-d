package org.czi.termolator.porting

/**
  *
  */
object abbreviate extends JepEnabled {

  import DataDef._

  val moduleName = "abbreviate"

  /**
    * @code_reference [[abbreviate.run_abbreviate_on_lines]]
    *
    *  @dataFlow write to [[ABBR]]
    *           https://github.com/SemanticBeeng/The_Termolator/blob/99192d6931510972b780f301405d11d37757ee66/abbreviate.py#L1294-L1294
    */
  def run_abbreviate_on_lines(lines : List[str],
                              abbr_file : File[ABBR],
                              reset_dictionary : Boolean = false) : List[Map[str, str]] = {

    import collection.JavaConverters._
    FunctionDef("run_abbreviate_on_lines", ("lines", lines), ("abbr_file", abbr_file), ("reset_dictionary", reset_dictionary)).
      pyCallAndReturn[java.util.List[Map[str, str]]]().asScala.toList
  }

  /**
    *
    */
  def save_abbrev_dicts(abbr_to_full_file : File[ABBR], full_to_abbr_file: File[ABBR]): Unit  = {

    FunctionDef("save_abbrev_dicts", ("abbr_to_full_file", abbr_to_full_file), ("full_to_abbr_file", full_to_abbr_file)).pyCall()
  }

  /**
    *
    */
  def record_abbreviate_dictionary = ???
}
