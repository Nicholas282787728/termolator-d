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

  case class FunctionDef(name: String, args: (String, Any)*) {
    /**
      *
      */
    def pyCall() = {

      ensureModuleInitialized()

      val callString = s"$name(${mapArgs(args)})"
      println(s"calling $moduleName.$callString")
      jep.eval(callString)
    }

    /**
      *
      */
    private def mapArgs(args: Seq[(String, Any)]) : String = {
      args.toList.map {
        case (n: String, v: String) ⇒ s"$n = `$v`"
        case (n: String, v: Boolean) ⇒ if (v) s"$n = True" else s"$n = False"
        case (n: String, v: Option[_]) ⇒ if (v.isDefined) mapArgs(Seq((n, v.get))) else s"$n = None"
        case (n: String, v: Seq[_]) ⇒ s"$n = [ ${mapArgs(Seq((n, v)))} ]"
        case (n: String, v: Any) ⇒ s"$n = ${v.toString}"
      }.mkString(", ")
    }

  }

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

}

