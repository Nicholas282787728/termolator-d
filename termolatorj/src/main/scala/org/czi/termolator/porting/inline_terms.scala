package org.czi.termolator.porting

import java.util

import scala.collection.immutable.Seq
import scala.collection.mutable


/**
  *
  */
object inline_terms extends JepEnabled {

  import DataDef._

  val moduleName = "inline_terms"

  /**
    * @code_reference [[./nyu-english-new/inline_terms.py:1562]]
    *
    */
  def make_term_chunk_file_list(infiles: List[(File[POS],  File[TERMS], File[ABBR])]
                                /*List[(FileName[POS], FileName[TERMS], FileName[ABBR])]*/,
                                no_head_terms_only: bool = False) : /*outfiles*/ List[File[TCHUNK]] = {

    infiles map { infile ⇒

      val chunk_file = make_term_chunk_file(pos_file = infile._1,
        term_file = infile._2,
        abbreviate_file = infile._3,
        no_head_terms_only = no_head_terms_only)

      chunk_file
    }
  }


  /**
    * @code_reference [[./nyu-english-new/inline_terms.py:1513]]
    *
    * @dataFlow @todo @dataFlow
    *          https://github.com/SemanticBeeng/The_Termolator/blob/5863972ba7e84d670dbdd6e89af467cc94a9b814/inline_terms.py#L1810-L1810
    *          https://github.com/SemanticBeeng/The_Termolator/blob/5863972ba7e84d670dbdd6e89af467cc94a9b814/inline_terms.py#L1828-L1828
    *          https://github.com/SemanticBeeng/The_Termolator/blob/5863972ba7e84d670dbdd6e89af467cc94a9b814/inline_terms.py#L1835-L1835
    *          https://github.com/SemanticBeeng/The_Termolator/blob/ebfb4b63d1d14766cb1fac6758bbae3b70191ec8/inline_terms.py#L1853-L1853
    */
  def make_term_chunk_file(pos_file : File[POS],
                           term_file : File[TERMS],
                           abbreviate_file : File[ABBR],
                           no_head_terms_only : bool = False) : File[TCHUNK] = {

    /**
      * @todo for [[term_file]]
      */
    term_utilities.get_integrated_line_attribute_value_structure_no_list

    /**
      * @todo for [[abbreviate_file]]
      */
    term_utilities.get_integrated_line_attribute_value_structure_no_list

    get_pos_structure(null) //@todo
    null //@todo
  }

  def get_pos_structure (line: str) = ???

  /**
    * @dataFlow write to [[TERMS]]
    *          https://github.com/SemanticBeeng/The_Termolator/blob/7ed860ac1209600e8d1c97b72169cf6f262ed2ff/inline_terms.py#L1735-L1735
    */
  def find_inline_terms(lines : List[str],
                        fact_file : File[FACT],
                        pos_file : File[POS],
                        terms_file : File[TERMS],
                        marked_paragraphs : Boolean = false,
                        filter_off : Boolean = false) : Unit = {

    FunctionDef("find_inline_terms",
      ("lines", lines), ("fact_file", fact_file),
      ("pos_file", pos_file),  ("terms_file", terms_file), ("marked_paragraphs", marked_paragraphs),
      ("filter_off", filter_off)).pyCall()
  }

  /**
    *
    */
  def get_topic_terms(text: str, offset: int, filter_off: bool=False) : List[(Long, Long, str)] = {

    import collection.JavaConverters._
    val r: Seq[util.List[_]] = FunctionDef("get_topic_terms", ("text", text), ("offset", offset), ("filter_off", filter_off)).
      pyCallAndReturn[util.List[util.List[_]]]().asScala.toList

    val r2: Seq[(Long, Long, String)] = r map { e ⇒
      val e1 = e.asScala
      print("koko" + e1)

      val e2: (Long, Long, String) = e1 match {
        case mutable.Buffer(a: java.lang.Long, b: java.lang.Long, c: str) ⇒ (Long.unbox(a), Long.unbox(b), c)
        case _ ⇒ assert(false); (0, 0, "")
      }
      e2
    }

    r2.toList
  }

//  FunctionDef("get_topic_terms", ("text", text), ("offset", offset), ("filter_off", filter_off)).
//    pyCallAndReturn[util.List[_]]().asScala.toList map {
//    _.asInstanceOf[java.util.List[_]].asScala.toList
//  } map {
//    case mutable.Buffer(a: java.lang.Long, b: java.lang.Long, c: str) ⇒ (a, b, c)
//    case _ ⇒ None; assert(false)
//  }

  /**
    *
    */
  def get_next_word(instring: str, start: int) : Option[(str, int, int)] = {
    None
  }
}
