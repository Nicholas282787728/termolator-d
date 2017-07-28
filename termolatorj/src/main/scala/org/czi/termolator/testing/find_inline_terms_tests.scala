package org.czi.termolator.testing

import org.czi.termolator.porting.{abbreviate, dictionary, find_terms, term_utilities}


/**
  *
  */
object find_inline_terms_tests extends App {

  term_utilities.ensureModuleInitialized()
  abbreviate.ensureModuleInitialized()
  find_terms.ensureModuleInitialized()
  dictionary.ensureModuleInitialized()

  dictionary.initialize_utilities()

  import org.czi.termolator.porting.RuntimeConfig._
  val file = NYU_DIR + "foreground/19729111"

  /**
    * @todo cannot assert anything about this becuase it is monolithical
    */
  find_terms.find_inline_terms_for(file, start = true)

}
