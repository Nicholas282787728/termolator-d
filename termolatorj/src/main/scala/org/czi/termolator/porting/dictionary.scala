package org.czi.termolator.porting

/**
  *
  */
object dictionary extends JepEnabled {

  val moduleName = "dictionary"

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
