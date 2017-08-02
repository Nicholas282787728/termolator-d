package org.czi.termolator.porting

import java.util.regex.{Matcher, Pattern}

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
  type Dict[K, V] = mutable.Map[K, V]
  // type DictM[K, V] = mutable.Map[K, V]
  type ListM[T] = mutable.ListBuffer[T]
  type Optional[T] = Option[T]
  type Tuple[T1, T2] = (T1, T2)
  type Tuple3[T1, T2, T3] = (T1, T2, T3)
  type Tuple4[T1, T2, T3, T4] = (T1, T2, T3, T4)
  type Pattern = java.util.regex.Pattern
  type Match = java.util.regex.Matcher

  val False = false
  val True = true
  val nullInt : int = 0L
  val nullStr : str = ""
  // val nullBool : bool = None

  def list[T1, T2](t : (T1, T2)) = {
    val l: mutable.ListBuffer[(T1, T2)] = new mutable.ListBuffer[(T1, T2)]()
    l.append(t)
    l
  }

  /**
    *
    */
  class StringDSL(value: str) {

    def in(map: Dict[str, _]): bool = map.contains(value)

    def in(list: Seq[Any]): bool = list.contains(value)

    def in(set: Set[str]): bool = set.contains(value)

    def upper() : str = value.toUpperCase

    def lower() : str = value.toLowerCase

    def endswith(suffix: str) : bool = value.endsWith(suffix)

    def isalpha(): bool = value.isalpha()

    def isupper(): bool = value.isupper()

    def slice(start: int, end: int) : str = {
      if(end > 0)
        value.substring(start.toInt, end.toInt)
      else
        value.substring(value.length - end.toInt)
    }

    def at(index : int) : Character = {
      if(index > 0)
        value.charAt(index.toInt)
      else
        value.charAt(value.length - index.toInt)
    }
  }

  implicit def string2StringDSL(value: str): StringDSL = new StringDSL(value)

  /**
    *
    */
  class CharDSL(value: Character) {

    def in(text: str) : bool = text.contains(value)

    def isalpha(): bool = value.isalpha()
  }

  implicit def char2CharDSL(value: Character): CharDSL = new CharDSL(value)

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

    def searchM(regex: Pattern, value: String): Matcher = {
      regex.matcher(value)
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

    def searchM(text: String): Matcher = re.searchM(value, text)
  }

  implicit def pattern2RegexDSL(value: Pattern): RegExDSL = new RegExDSL(value)

  def len(list: Seq[Any]) = list.size

  def str(o : int) = o.toString

  def str(o : Object) = o.toString

  def isDefined(o: Any) = {
    o match {
      case o1: Option[_]  ⇒ o1.isDefined
      case o1: Match      ⇒ o1.matches()
      case o1             ⇒ o1 != null
    }
  }

  val pass = Unit
}
