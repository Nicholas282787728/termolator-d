package org.czi.termolator.porting

import jep.{Jep, JepConfig}


/**
  *
  */
trait JepEnabled {

  import RuntimeConfig._

  val config = new JepConfig
  config.addIncludePaths(Array(".", root):_*)

  val jep = new Jep(config)
  var moduleInited: Boolean = false

  /**
    *
    */
  private def ensureModuleInitialized(): Unit = {
    if (!moduleInited) {
      jep.set("__file__", root + "/another")
      runScript(s"$moduleName.py")
      moduleInited = true
    }
  }

  /**
    *
    */
  def moduleName: String

  def runScript(functinName : String) = {
    jep.runScript(root + functinName)
  }

  /**
    *
    */
  def pyCall(functionName: String, args: Any*) = {

    ensureModuleInitialized()

    val callString = s"$functionName(${mapArgs(args)})"
    println(s"calling $moduleName.$callString")
    jep.eval(callString)
  }

  /**
    *
    */
  private def mapArgs(args: Seq[Any]) : String = {
    args.toList.map {
      case a: String ⇒ s"`$a`"
      case a: Boolean ⇒ if (a) "True" else "False"
      case a: Option[_] ⇒ if (a.isDefined) mapArgs(Seq(a.get)) else "None"
      case a: Seq[_] ⇒ s"[ ${mapArgs(a)} ]"
      case a ⇒ a.toString
    }.mkString(", ")
  }
}

