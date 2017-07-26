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

  case class FunctionDef(name: String, args: (String, Any)*)

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
  def pyCall(funDef : FunctionDef) = {

    ensureModuleInitialized()

    val callString = s"${funDef.name}(${mapArgs({funDef.args})})"
    println(s"calling $moduleName.$callString")
    jep.eval(callString)
  }

  /**
    *
    */
  private def mapArgs(args: Seq[(String, Any)]) : String = {
    args.toList.map {
      case (n: String, v: String) ⇒ s"`$v`"
      case (n: String, v: Boolean) ⇒ if (v) "True" else "False"
      case (n: String, v: Option[_]) ⇒ if (v.isDefined) mapArgs(Seq((n, v.get))) else "None"
      case (n: String, v: Seq[_]) ⇒ s"[ ${mapArgs(Seq((n, v)))} ]"
      case (n: String, v: Any) ⇒ v.toString
    }.mkString(", ")
  }
}

