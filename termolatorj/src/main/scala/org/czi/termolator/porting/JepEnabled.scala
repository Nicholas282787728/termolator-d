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

      val vals = argsValues
      val callString = s"$func(${vals.mkString(", ")})"
      println(s"calling $moduleName.$callString")

      invokeWith(vals : _*)
      //      if(vals.nonEmpty)
      //        jep.invokeWith(func, vals:_*)
      //      else
      //        jep.invokeWith(func)
    }

    /**
      *
      */
    //var callCount = 1

    def pyCallAndReturn[T](): T = {

      ensureModuleInitialized()

      val vals = argsValues
      val callString = s"$func(${vals.mkString(", ")})"
      // val callString = s"$moduleName.$name(${mapArgs(args)})"
      println(s"calling $callString")

      //val varName = s"var_$func$callCount"
      //      jep.eval(s"$varName = $callString")
      //      jep.getValue(varName).asInstanceOf[T]
      //jep.invokeWith(func, vals).asInstanceOf[T]

      invokeWith(vals : _*).asInstanceOf[T]
      //      if(vals.nonEmpty)
      //        jep.invokeWith(func, vals:_*).asInstanceOf[T]
      //      else
      //        jep.invokeWith(func).asInstanceOf[T]
    }

    //    /**
    //      *
    //      */
    //    private def mapArgs(args: Seq[(String, Object)]) : String = {
    //      args.toList.map {
    //        case (n: String, v: String) ⇒ s"$n = `$v`"
    //        case (n: String, v: Boolean) ⇒ if (v) s"$n = True" else s"$n = False"
    //        case (n: String, v: Option[_]) ⇒ if (v.isDefined) mapArgs(Seq((n, v.get))) else s"$n = None"
    //        case (n: String, v: Seq[_]) ⇒ s"$n = [ ${mapArgs(Seq((n, v)))} ]"
    //        case (n: String, v: Any) ⇒ s"$n = ${v.toString}"
    //        case (n: String, null) ⇒ s"$n = None"   // @todo unsure how to do this better
    //        case _ ⇒ ""           // sot sure what this is but hoping for the best
    //      }.mkString(", ")
    //    }

    /**
      *
      */
    private def argsValues[T] = {

      import collection.JavaConverters._

      args map { _._2.asInstanceOf[AnyRef] } map {
        case arg: List[_] ⇒ arg.asJava

        case arg ⇒ arg
      }
    }

    private def invokeWith(vals: Object*): Object = {

        if(vals.nonEmpty)
          jep.invoke(func, vals.toArray : _*)
        else
          jep.invoke(func)
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

  def runScript(functinName: String) = {
    jep.runScript(root + functinName)
  }

}

