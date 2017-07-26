package org.czi.termolator.porting

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
                                no_head_terms_only: Boolean = false) : /*outfiles*/ List[File[TCHUNK]] = {

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
                           no_head_terms_only : Boolean = false) : File[TCHUNK] = {

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

  def get_pos_structure (line: String) = ???

  /**
    * @dataFlow write to [[TERMS]]
    *          https://github.com/SemanticBeeng/The_Termolator/blob/7ed860ac1209600e8d1c97b72169cf6f262ed2ff/inline_terms.py#L1735-L1735
    */
  def find_inline_terms(lines : List[String],
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

}
