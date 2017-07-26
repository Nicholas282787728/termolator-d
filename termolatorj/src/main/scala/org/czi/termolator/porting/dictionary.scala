package org.czi.termolator.porting

/**
  *
  */
object dictionary extends JepEnabled {

  val moduleName = "dictionary"


  def initialize_utilities() = {
    val functionName = "initialize_utilities"

    //jep.eval("dictionary.initialize_utilities()")

    pyCall(functionName)

  }

}
