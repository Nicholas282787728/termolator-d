package org.czi.termolator.porting

import jep.{Jep, JepConfig}


object JepContext {

  import RuntimeConfig._

  val config = new JepConfig
  config.addIncludePaths(Array(".", root):_*)

  val jep = new Jep(config)
  var moduleInited: Boolean = false

  def close = jep.close()
}

/**
  *
  */
trait JepEnabled {

  import RuntimeConfig._
  import JepContext._

  case class FunctionDef(name: String, args: (String, Any)*) {
    /**
      *
      */
    def pyCall() : Unit = {

      ensureModuleInitialized()

      val callString = s"$name(${mapArgs(args)})"
      println(s"calling $moduleName.$callString")
      jep.eval(callString)
    }

    /**
      *
      */
    var callCount = 1

    def pyCallAndReturn[T]() : T = {

      ensureModuleInitialized()

      val callString = s"$moduleName.$name(${mapArgs(args)})"
      println(s"calling $callString")

      val varName = s"var_$name$callCount"
      jep.eval(s"$varName = $callString")
      jep.getValue(varName).asInstanceOf[T]
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
        case (n: String, null) ⇒ s"$n = None"   // @todo unsure how to do this better
        case _ ⇒ ""           // sot sure what this is but hoping for the best
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

