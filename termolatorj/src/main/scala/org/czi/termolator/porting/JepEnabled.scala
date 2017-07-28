package org.czi.termolator.porting

import jep.{Jep, JepConfig}


/**
  *
  */
object JepContext {

  import RuntimeConfig._


  val config = new JepConfig
  config.addIncludePaths(Array(".", root): _*)

  val jep = new Jep(config)

  def close = jep.close()
}

/**
  *
  */
trait JepEnabled {

  import JepContext._
  import RuntimeConfig._


  var moduleInited: Boolean = false

  case class FunctionDef(func: String, args: (String, Any)*) {
    /**
      *
      */
    def pyCall(): Unit = {

      ensureModuleInitialized()

      val vals = argsValues(args)
      val callString = s"$func(${printArgs(args)})"
      println(s"\nCalling $callString")

      invokeWith(vals : _*)
    }

    /**
      *
      */
    val sep = "\n\t\t"

    def pyCallAndReturn[T](): T = {

      ensureModuleInitialized()

      val vals = argsValues(args)
      val callString = s"$func($sep${printArgs(args)}$sep)"
      println(s"calling $callString")

      invokeWith(vals : _*).asInstanceOf[T]
    }

    /**
      *
      */
    private def mapArgs(args: Seq[(String, Any)]): Seq[(String, Any/*, String*/)] = {

      import collection.JavaConverters._
      args.map {
        case (n: String, v: File[_])    ⇒ (n, v)
        case (n: String, v: String)     ⇒ (n, v)
        case (n: String, v: Boolean)    ⇒ (n, if(v) java.lang.Boolean.TRUE else java.lang.Boolean.FALSE)
        case (n: String, v: Option[_])  ⇒ (n, if (v.isDefined) mapArgs(Seq((n, v.get))) else (n, "None"))
        case (n: String, v: Seq[_])     ⇒ (n, v.asJava)
        case (n: String, v: Any)        ⇒ (n, v.toString)
        case (n: String, null)          ⇒ (n,  "None")      // @todo unsure how to do this better
        case (n, v)                     ⇒ (n, v)            // sot sure what this is but hoping for the best
      }
    }

    private def printArgs(args: Seq[(String, Any)]) : String  = {
      args.map {
        case (n: String, v: File[_])    ⇒ s"$n = ${v.toString}"
        case (n: String, v: String)     ⇒ s"$n = '$v'"
        case (n: String, v: Boolean)    ⇒ s"$n = $v"
        case (n: String, v: Option[_])  ⇒ s"$n = todo"
        case (n: String, v: Seq[_])     ⇒ s"$n = [$sep\t${v.mkString(s",\t\t\t\t ")}]"
        case (n: String, v: Any)        ⇒ s"$n = ${v.toString}"
        case (n: String, null)          ⇒ s"$n = None"      // @todo unsure how to do this better
        case (n, v)                     ⇒ s"$n = ??$v??"    // sot sure what this is but hoping for the best
      }.mkString(s", $sep")
    }
    /**
      *
      */
    private def argsValues[T](args: Seq[(String, Any)]): Seq[AnyRef] = {

      val mapped = mapArgs(args)
      mapped map { a ⇒ a._2.asInstanceOf[AnyRef] }
    }

    /**
      *
      */
    private def invokeWith(vals: Object*): Object = {

        if(vals.nonEmpty)
          jep.invoke(func, vals : _*)
        else
          jep.invoke(func)
    }
  }

  /**
    *
    */
  def ensureModuleInitialized(): Unit = {

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

  def runScript(functinName: String) = {
    jep.runScript(root + functinName)
  }

}

