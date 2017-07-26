package org.czi.termolator.porting

/**
  *
  */
object dictionary extends JepEnabled {

  val moduleName = "dictionary"


  def initialize_utilities() = {
    val functionName = FunctionDef("initialize_utilities")

    pyCall(functionName)

  }

}
