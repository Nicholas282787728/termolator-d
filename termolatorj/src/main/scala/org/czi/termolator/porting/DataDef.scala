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
  type jepInt = java.lang.Long
  type jepStr = String
  type jepTuple = java.util.List[_]
  def jepUnbox(i: jepInt) : int = Long.unbox(i)
  val False = false
  val nullInt : int = 0L
  val nullStr : str = ""

}
