package org.czi.termolator.porting

import java.util.regex.Pattern

import scala.collection.mutable
import scala.language.implicitConversions

object DataDef {

  type TXT = String
  type BARE = String
  type TXT2 = String
  type TXT3 = String
  type POS = String
  type FACT = String
  type TERMS = String
  type ABBR = String
  type TCHUNK = String
  type TCHUNK_NPS = String
  //type NPOS = String

  /**
    * Python type aliases
    */
  type str = String
  type int = Long
  type bool = Boolean
  type Dict[K, V] = Map[K, V]
  type Optional[T] = Option[T]
  type Tuple[T1, T2] = (T1, T2)
  type Tuple[T1, T2, T3] = (T1, T2, T3)
  type Tuple[T1, T2, T3, T4] = (T1, T2, T3, T4)
  type Pattern = java.util.regex.Pattern

  val False = false
  val True = true
  val nullInt : int = 0L
  val nullStr : str = ""
  // val nullBool : bool = None

  /**
    *
    */
  class StringDSL(value: str) {

    def in(map: Dict[str, _]): bool = map.contains(value)

    def in(list: Seq[Any]): bool = list.contains(value)

    def in(set: Set[Any]): bool = set.contains(value)

    def upper() : str = value.toUpperCase

    def lower() : str = value.toLowerCase

    def endswith(suffix: str) : bool = value.endsWith(suffix)

    def isalpha(): bool = value.isalpha()

    def slice(start: int, end: int) : str = {
      if(end > 0)
        value.substring(start.toInt, end.toInt)
      else
        value.substring(value.length - index.toInt)
    }

    def at(index : int) : str = {
      if(index > 0)
        value.charAt(index)
      else
        value.charAt(value.length - index.toInt)
    }
  }

  implicit def string2StringDSL(value: str): StringDSL = new StringDSL(value)

  /**
    *
    */
  class CharDSL(value: char) {

    def in(text: str) : bool = text.contains(value)
  }

  implicit def char2CharDSL(value: char): CharDSL = new CharDSL(value)

  /**
    *
    */
  class BooleanDSL(value: bool) {
    def and(another: bool) = value && another

    def or(another: bool) = value || another

    def not() = !value
  }

  def not(value : bool) = !value
  implicit def bool2BoolDSL(value: bool): BooleanDSL = new BooleanDSL(value)

  /**
    *
    */
  class ListDSL[T](value: mutable.ListBuffer[T]) {

    def append(another: T) = value += another

  }

  implicit def list2ListDSL[T](value: mutable.ListBuffer[T]): ListDSL[T] = new ListDSL[T](value)

  /**
    *
    */
  object jep {
    type int = java.lang.Long
    type str = String
    type tuple = java.util.List[_]
    def unbox(i: int) : Long = Long.unbox(i)
  }

  object os {
    val linesep = "\n"
  }

  /**
    *
    */
  object re {

    val I: Int = 0

    def quote(regex : String): String = {
      Pattern.quote(regex)
    }

    def compile(regex: String, flags: Int = 0): Pattern = {
      /**
        * @todo https://stackoverflow.com/a/10502921/4032515 quoting in Java vs Python
        */
      Pattern.compile(quote(regex), flags)
    }

    def search(regex: String, value: String): bool = {
      Pattern.compile(regex).matcher(value).find
    }

    def search(regex: String, value: Char): bool = {
      Pattern.compile(regex).matcher(value.toString).find
    }

    def search(regex: Pattern, value: String): bool = {
      regex.matcher(value).find
    }

    def sub(from: str, to: str, in: str) : str = {
      ""
    }
  }

  /**
    *
    */
  class RegExDSL(value: Pattern) {
    def search(text: String): bool = re.search(value, text)
  }

  implicit def pattern2RegexDSL(value: Pattern): RegExDSL = new RegExDSL(value)

  def len(list: Seq[Any]) = list.size

  def str(o : Object) = o.toString

  def isDefined(o: Any) = {
    o match {
      case o1: Option[_] ⇒ o1.isDefined
      case o1 ⇒ o1 != null
    }
  }

  val pass = Unit
}
