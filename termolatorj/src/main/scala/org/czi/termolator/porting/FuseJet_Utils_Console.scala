package org.czi.termolator.porting

import DataDef.{FACT, File, POS, TXT3}


/**
  * Created by nickdsc on 7/23/17.
  */
object FuseJet_Utils_Console {

  /**
    * @dataFlow writes [[POS]] files
    *          https://github.com/SemanticBeeng/The_Termolator/blob/2895dccd653a83dd023c86f8b27e6678dc9c5d2b/tests/czi/utils.sh#L85-L85
    */
  def main(filelist: File[(File[TXT3], File[FACT])]): File[File[POS]] = {
    // @todo
    null
  }
}
