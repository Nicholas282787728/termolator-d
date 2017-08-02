package org.czi.termolator.porting

import java.util

import scala.collection.mutable


/**
  *
  */
trait inline_terms_intf extends JepEnabled {

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
                        marked_paragraphs : bool = False,
                        filter_off : bool = False) : Unit = {

    FunctionDef("find_inline_terms",
      ("lines", lines), ("fact_file", fact_file),
      ("pos_file", pos_file),  ("terms_file", terms_file), ("marked_paragraphs", marked_paragraphs),
      ("filter_off", filter_off)).pyCall()
  }

  /**
    * Really must do this to avoid having to reference Jep specifics in client code
    * For example Jep seems to map Python Tuples to [[mutable.Buffer]]
    *
    * @todo try a more generic solution with
    *       https://stackoverflow.com/a/19901310/4032515
    *
    * @todo how would I do this from Java??
    *       "So it is clear that Java has tuples, but we can use them only as function's arguments
    *       and not for function's return values."
    *       https://dzone.com/articles/whats-wrong-java-8-part-v
    *
    */
  def get_topic_terms(text: str, offset: int, filter_off: bool=False) : List[(int, int, str)] = {

    import collection.JavaConverters._
    FunctionDef("get_topic_terms", ("text", text), ("offset", offset), ("filter_off", filter_off)).
      pyCallAndReturn[util.List[jep.tuple]]().asScala.toList map { e ⇒ e.asScala match {
        case mutable.Buffer(_1: jep.int, _2: jep.int, _3: jep.str) ⇒ (jep.unbox(_1), jep.unbox(_2), _3)
        case _ ⇒ assert(false); (nullInt, nullInt, nullStr)
      }
    }
  }

  /**
    *
    */
   def get_formulaic_term_pieces(text: str, offset: int) : List[Tuple4[int, int, str, str]] = {
      import collection.JavaConverters._
      FunctionDef("get_formulaic_term_pieces", ("text", text), ("offset", offset)).
        pyCallAndReturn[util.List[jep.tuple]]().asScala.toList map { e ⇒
        e.asScala match {
          case mutable.Buffer(_1: jep.int, _2: jep.int, _3: jep.str, _4: jep.str) ⇒ (jep.unbox(_1), jep.unbox(_2), _3, _4)
          case _ ⇒ assert(false); (nullInt, nullInt, nullStr, nullStr)
        }
      }
   }

  /**
    *
    */
  def merge_formulaic_and_regular_term_tuples(term_tuples: List[Tuple3[int, int, str]], formulaic_tuples: List[Tuple4[int, int, str, str]])
    : List[Tuple4[int, int, str, str]] = {

      import collection.JavaConverters._
      FunctionDef("merge_formulaic_and_regular_term_tuples", ("term_tuples", term_tuples), ("formulaic_tuples", formulaic_tuples)).
        pyCallAndReturn[util.List[jep.tuple]]().asScala.toList map { e ⇒
        e.asScala match {
          case mutable.Buffer(_1: jep.int, _2: jep.int, _3: jep.str, _4: jep.str) ⇒ (jep.unbox(_1), jep.unbox(_2), _3, _4)
          case _ ⇒ assert(false); (nullInt, nullInt, nullStr, nullStr)
        }
      }
  }

  /**
    *
    */
  def get_next_word(instring: str, start: int) : Option[(str, int, int)] = {
    None
  }

  /**
    *
    */
  def topic_term_ok_boolean(word_list: List[str], pos_list: List[str], term_string: str) : bool = {

    FunctionDef("topic_term_ok_boolean", ("word_list", word_list), ("pos_list", pos_list), ("term_string", term_string)).
      pyCallAndReturn[bool]()
    }

    /**
     *
     */
    def load_pos_offset_table(pos_file: File[POS]) : Unit = {
      FunctionDef("load_pos_offset_table", ("pos_file", pos_file)).pyCall()
    }

   /**
    *
    */
    def global_formula_filter(term_list: List[str], term_hash: Dict[str, List[Tuple[int, int]]], term_type_hash: Dict[str, str]) : Unit = {
      FunctionDef("global_formula_filter", ("term_list", term_list), ("term_hash", term_hash), , ("term_type_hash", term_type_hash)).pyCall()
    }
}


object inline_terms extends inline_terms_intf