package org.czi.termolator.porting

import scala.io.Source

object DataDef {

  type TXT = String
  type BARE = String
  type TXT2 = String
  type TXT3 = String
  type POS = String
  type FACT = String
  type TERMS = String
  type ABBR = String
  type TCHUNK = String
  type TCHUNK_NPS = String
  //type NPOS = String

  /**
    * Python type aliases
    */
  type str = String
  type int = Long
  type bool = Boolean

  val False = false
  val nullInt : int = 0L
  val nullStr : str = ""
  // val nullBool : bool = None

  object jep {
    type int = java.lang.Long
    type str = String
    type tuple = java.util.List[_]
    def unbox(i: int) : Long = Long.unbox(i)
  }


}
