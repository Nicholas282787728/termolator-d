package org.czi.termolator.porting

/**
  *
  */
object abbreviate {

  import DataDef._

  /**
    * @code_reference [[abbreviate.run_abbreviate_on_lines]]
    *
    *  @dataFlow write to [[ABBR]]
    *           https://github.com/SemanticBeeng/The_Termolator/blob/99192d6931510972b780f301405d11d37757ee66/abbreviate.py#L1294-L1294
    */
  def run_abbreviate_on_lines(lines : List[String],
                              abbr_file : File[ABBR],
                              reset_dictionary : Boolean = false) = _

  def save_abbrev_dicts(abbr_to_full_file : File[ABBR], full_to_abbr_file: File[ABBR]) = _

  /**
    *
    */
  def record_abbreviate_dictionary = _
}
