package org.czi.termolator.porting

/**
  *
  */
object run_make_term_chunk {

  import DataDef._
  import run_termolator._

  /**
    * @code_reference [[./nyu-english-new/run_make_term_chunk.py:8]]
    *
    *                 [[internal_pos_terms_abbr_list]] -> [[internal_foreground_tchunk_list]]
    *                 [[internal_pos_terms_abbr_list @todo FIX THIS TO BE BACKGROUND]] -> [[internal_background_tchunk_list]]
    */
  def main(infiles: File[(File[POS],  File[TERMS], File[ABBR])]
           /*List[(FileName[POS], FileName[TERMS], FileName[ABBR])]*/) : File[File[TCHUNK]] = {

    // @todo inline_terms.make_term_chunk_file_list(infiles)

    internal_foreground_tchunk_list //@todo
  }
}
