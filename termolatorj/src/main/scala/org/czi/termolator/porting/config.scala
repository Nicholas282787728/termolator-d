package org.czi.termolator.porting

import scala.collection.mutable


/**
  * Created by nickdsc on 8/1/17.
  */
object config {

  import DataDef._

  val nom_dict: Dict[str, str] = new mutable.HashMap[str, str]()
  val pos_dict: Dict[str, List[str]] = new mutable.HashMap[str, List[str]]()


}
