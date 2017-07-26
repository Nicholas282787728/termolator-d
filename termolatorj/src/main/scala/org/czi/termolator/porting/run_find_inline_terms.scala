package org.czi.termolator.porting


/**
  * Created by nickdsc on 7/12/17.
  */
object run_find_inline_terms {

  import DataDef._
  import run_termolator_j._

  /**
    * [[internal_prefix_list]]
    */
  def main(files: File[File[BARE]], output_file_name: String, topic_areas : List[String]) = {

    find_terms.find_inline_terms_for_file_list(null, false) //@todo
  }


}
