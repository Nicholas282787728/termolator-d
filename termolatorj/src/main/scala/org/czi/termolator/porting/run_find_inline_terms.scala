package org.czi.termolator.porting


/**
  *
  */
object run_find_inline_terms {

  import DataDef._
  import run_termolator._

  /**
    * [[internal_prefix_list]]
    */
  def main(files: File[File[BARE]], output_file_name: String, topic_areas : List[String]) = {

    dictionary.initialize_utilities()
    find_terms.find_inline_terms_for_file_list(null, None) //@todo
  }


}
