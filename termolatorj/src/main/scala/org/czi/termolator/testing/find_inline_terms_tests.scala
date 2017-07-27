package org.czi.termolator.testing

import org.czi.termolator.porting.{dictionary, find_terms}


/**
  *
  */
class find_inline_terms_tests extends App {

  dictionary.initialize_utilities()

  import org.czi.termolator.porting.RuntimeConfig._
  val file = NYU_DIR + "foreground/19729111"

  /**
    * @todo cannot assert anything about this becuase it is monolithical
    */
  find_terms.find_inline_terms_for(file, true)

}
