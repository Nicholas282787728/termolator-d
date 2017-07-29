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
    * @todo more files to terst: difference in [[org.czi.termolator.porting.DataDef.TERMS]] files
    */
  private val DAVETEST_all_root = "/development/projects/04_clients/czi/ds/The_Termolator/tests/czi/DAVETEST_all/source/"
  DAVETEST_all_root + "foreground/26718012.terms"
  DAVETEST_all_root + "foreground/26717674.terms"
  DAVETEST_all_root + "foreground/26717671.terms"
  DAVETEST_all_root + "foreground/26717670.terms"
  DAVETEST_all_root + "foreground/26717663.terms"
  DAVETEST_all_root + "foreground/19669636.terms"

  /**
    * @todo cannot assert anything about this becuase it is monolithical
    */
  find_terms.find_inline_terms_for(file, start = true)

}
