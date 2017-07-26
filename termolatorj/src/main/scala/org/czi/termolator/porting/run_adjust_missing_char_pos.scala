package org.czi.termolator.porting

/**
  * Created by nickdsc on 7/12/17.
  */
object run_adjust_missing_char_pos {

  import DataDef._
  import run_termolator._


  /**
    * [[internal_fact_pos_list]]
    */
  def main(input: File[(File[FACT], File[POS])]) = _ {
    fix_bad_char_in_file(null, null) //@todo
  }

  /**
    * @code_reference [[./nyu-english-new/run_adjust_missing_char_pos.py:38]]
    *
    * @dataFlow @todo write to [[POS]]
    *          https://github.com/SemanticBeeng/The_Termolator/blob/99dcaa723dfc443c5ba70a10de65abe00f3ebe4a/run_adjust_missing_char_pos.py#L82-L82
    *          https://github.com/SemanticBeeng/The_Termolator/blob/99dcaa723dfc443c5ba70a10de65abe00f3ebe4a/run_adjust_missing_char_pos.py#L88-L88
    *          https://github.com/SemanticBeeng/The_Termolator/blob/99dcaa723dfc443c5ba70a10de65abe00f3ebe4a/run_adjust_missing_char_pos.py#L90-L90
    */
  private def fix_bad_char_in_file(fact: File[FACT], pos: File[POS]) = {
    get_pos_facts(null) //@todo

    make_fact_pair

    make_pos_triple

    modify_pos_end
  }

  /**
    * @code_reference [[./nyu-english-new/run_adjust_missing_char_pos.py:7]]
    */
  private def get_pos_facts(facts: List[FACT]) = _

  /**
    * @code_reference [[./nyu-english-new/run_adjust_missing_char_pos.py:20]]
    */
  private def make_fact_pair = _


  /**
    * @code_reference [[./nyu-english-new/run_adjust_missing_char_pos.py:20]]
    */
  private def make_pos_triple = _

  /**
    * @code_reference [[./nyu-english-new/run_adjust_missing_char_pos.py:29]]
    */
  private def modify_pos_end = _
}
