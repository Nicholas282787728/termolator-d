package org.czi.termolator.porting

import org.czi.termolator.porting.DataDef.Dict


/**
  *
  */
object dictionary extends JepEnabled {

  val moduleName = "dictionary"

  /**
    *
    */
  def freeze_dict[K, V](d: Dict[K, V]) = d


  /**
    *
    */
  def initialize_utilities() = {
    FunctionDef("initialize_utilities").pyCall()

  }

  /**
    *
    */
  def read_in_noun_morph_file() : Unit = {
    FunctionDef("read_in_noun_morph_file").pyCall()
  }

  /**
    *
    */
  def read_in_nom_dict() : Unit = {
    FunctionDef("read_in_nom_dict").pyCall()
  }
}
