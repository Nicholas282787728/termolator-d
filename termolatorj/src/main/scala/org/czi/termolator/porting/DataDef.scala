package org.czi.termolator.porting

/**
  * rm -rf `find . -name *.txt2`
*rm -rf `find . -name *.txt3`
*rm -rf `find . -name *.pos`
*rm -rf `find . -name *.terms`
*rm -rf `find . -name *.abbr`
*rm -rf `find . -name *.fact`
*rm -rf `find . -name *.tchunk`
*rm -rf `find . -name *.tchunk.nps`
 *
 */

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
    * Represents a persistent list of records of type [[T]]s
    */
  case class File[T](name: String) {
    def items: List[T] = _
  }

//  type Records[T] = List[Record[T]]
//  type Records2[T1, T2] = List[Record2[T1, T2]]
//  type Records3[T1, T2, T3] = List[Record3[T1, T2, T3]]

  type FileList = Array[String]

}
