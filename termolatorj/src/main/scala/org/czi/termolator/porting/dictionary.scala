package org.czi.termolator.porting

/**
  *
  */
object dictionary extends JepEnabled {

  val moduleName = "dictionary"


  def initialize_utilities() = {
    FunctionDef("initialize_utilities").pyCall()

  }

}
