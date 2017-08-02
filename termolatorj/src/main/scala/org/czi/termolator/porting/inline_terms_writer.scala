package org.czi.termolator.porting


import scala.collection.immutable.Seq
import scala.collection.mutable
import scala.language.implicitConversions

//
//   Perists the TERMSS for a single source "file"
//

import org.czi.termolator.porting.DataDef._


object inline_terms_writer {


  class TermsWriter {

    object Patterns {
      val et_al_citation: Pattern = re.compile(" et[.]? al[.]? *$")
    }

    private var term_id_number: int = 0
    private var outstream: File[TERMS] = _

//    def this(is: File[TERMS]) = {
//      this.outstream = os
//      this.term_id_number = 0
//    }

    //
    // @semanticbeeng @dataFlow
    //
    def write_all(term_list: List[str], lemmer: inline_terms_lemmer.TermsLemmer): Unit = {
      // @semanticbeeng @sideEffect  ensure no mutations from here on
      val term_hash: Dict[str, List[Tuple[int, int]]] = lemmer.term_hash.asInstanceOf[Dict[str, List[Tuple[int, int]]]] //@todo hack
      val term_type_hash: Dict[str, str] = dictionary.freeze_dict(lemmer.term_type_hash)
      val head_hash: Dict[str, str] = dictionary.freeze_dict(lemmer.head_hash)
      val lemma_dict: Dict[str, str] = dictionary.freeze_dict(lemmer.lemma_dict)
      val lemma_count: Dict[str, int] = dictionary.freeze_dict(lemmer.lemma_count)

      for (term <- term_list) {

        if ((term in term_type_hash) and !(term_type_hash(term) in List(false, "chunk-based")))
          this.__write_term_summary_fact_set(term, term_hash(term),
            lemma_dict, lemma_count,
            head_term = Some(term.upper()),
            head_lemma = Some(term.upper()),
            term_type = Some(term_type_hash(term)))

        else if (Patterns.et_al_citation.search(term))
          this.__write_term_becomes_article_citation(term, term_hash(term))

        else if (term_utilities.org_ending_pattern.search(term) or this.org_head_ending(term, head_hash))
          this.__write_term_becomes_organization(term, term_hash(term))

        else if (term_utilities.person_ending_pattern.search(term))
          this.__write_term_becomes_person(term, term_hash(term))

        else {
          if (this.__term_is_org_with_write(term, term_hash(term))) {
            pass
          } else {

            var head_term: str = null
            var head_lemma: str = null

            if (term in head_hash) {
              val head_term: str = head_hash(term)
              if (head_term in lemma_dict)
                head_lemma = lemma_dict(head_term)

              else if (head_term in term_type_hash)
                head_lemma = lemmer.get_term_lemma(head_term, term_type = Some(term_type_hash(head_term)))
              else
                head_lemma = lemmer.get_term_lemma(head_term)

            } else {
              head_term = null //None //  @semanticbeeng @todo static typing
              head_lemma = null //None //  @semanticbeeng @todo static typing
            }
            //   @semanticbeeng @todo @dataFlow
            this.__write_term_summary_fact_set(term, term_hash(term), lemma_dict, lemma_count,
              head_term = Some(head_term), head_lemma = Some(head_lemma))
          }
        }
      }
    }

    //
    //   @semanticbeeng @todo
    //
    def __term_is_org_with_write(term: str, instances: List[Tuple[int, int]]): bool = {

      if (not (re.search("[A - Z] ", term.charAt(0)))) {
        return (false)
      }

      val words: Seq[(int, str)] = term_utilities.divide_sentence_into_words_and_start_positions(term)
      var person_names = 0
      var Fail = false
      var ambiguous_person_names = 0
      val word_pattern = mutable.ListBuffer[str]()
      var ends_in: str = null

      if (re.search("^[A - Z][a - z]", words(-1)._2)) {
        if (term_utilities.last_word_organization.search(words(-1)._2))
          ends_in = "ORG"

        else if (term_utilities.last_word_gpe.search(words(-1)._2))
          ends_in = "GPE"

        else if (term_utilities.last_word_loc.search(words(-1)._2))
          ends_in = "LOC"
      } else
        ends_in = null //None // @semanticbeeng @todo static typing

      for ((position, word) ← words) {
        val lower = word.lower()
        val is_capital = re.search("^[A - Z][a - z]", word)

        if (is_capital and (lower in config.pos_dict) and ("PERSON_NAME" in config.pos_dict(lower))) {
          person_names = person_names + 1

          if (len(config.pos_dict(lower)) > 1) {
            ambiguous_person_names = ambiguous_person_names + 1
            word_pattern.append("ambig_name")
          }
          else
            word_pattern.append("name")
        }

        if (is_capital or term_utilities.closed_class_check2.search(word)) {
          pass
        }
        else
          Fail = true
      }

      var length_name_criterion: bool = False
      if (not (term_utilities.ambig_last_word_org.search(words(-1)._2)))
        length_name_criterion = True
      else if ((len(words) < 4) or ((person_names > 1) and (person_names > ambiguous_person_names)))
        length_name_criterion = True
      else
        length_name_criterion = False

      var ne_class: str = null
      if ((len(words) <= 1) or (not (" " in term)))
        return (False)
      else if ((ends_in == "ORG ") and length_name_criterion)
        ne_class = "ORGANIZATION"
      else if ((ends_in == "GPE ") and length_name_criterion)
        ne_class = "GPE"
      else if ((ends_in == "LOC ") and length_name_criterion)
        ne_class = "LOCATION"
      else if (person_names == 0)
        return (false)
      else if ((len(words) == 2)
               and (person_names == 2)
               and (person_names > ambiguous_person_names)
               and (" " in term)
               and (word_pattern.last == "name")) {
        //// all words of an organization except for closed class words should
        //// be capitalized.
        //// However, 2 word capitalized phrases can be person names, particularly if
        //// both words are in our person dictionary, so let's ! include these
        //// If first word is a name & second word is a non-name, probably this is !
        //// an organization.
        ne_class = "ORGANIZATION_OR_GPE "
      }
      else if (Fail)
        return (false)
      else
      //// ne_class = 'ORGANIZATION'
        return (false)

      // global term_id_number @semanticbeeng @global state
      for ((start, end) ← instances) {
        this.term_id_number = 1 + this.term_id_number
        this.outstream.write(ne_class + " ID = \"NYU_ID_" + str(this.term_id_number) + "\" STRING = \"" + term + "\"")
        this.outstream.write(" START =" + str(start) + " END =" + str(end) + os.linesep)
      }
      return (true)
    }

    //
    //   @semanticbeeng @todo static type
    //
    def __write_term_summary_fact_set(term: str, instances: List[Tuple[int, int]],
                                       lemma_dict: Dict[str, str], lemma_count: Dict[str, int],
                                       head_term: Optional[str] = None, head_lemma: Optional[str] = None,
                                       term_type: Optional[str] = None
                                     ): Unit = {
      // global term_id_number @semanticbeeng global state
      val frequency = len(instances)
      val lemma = lemma_dict(term)
      val lemma_freq = lemma_count(lemma)

      for ((start, end) ← instances) {
        this.term_id_number = 1 + this.term_id_number

        if (term_type.get == "url") {
          this.outstream.write("URL ID=\"NYU_TERM_\"" + str(this.term_id_number) +
                               "\" STRING = \"" + this.term_string_edit(term) +
                               "\" FREQUENCY = " + str(frequency))
        }
        else {
          this.outstream.write("TERM ID = \"NYU_TERM_" + str(this.term_id_number) +
                               "\" STRING = \"" + this.term_string_edit(term) +
                               "\"" + " FREQUENCY = " + str(frequency))
        }

        this.outstream.write(" START = " + str(start) + " END =" + str(end))
        this.outstream.write(" LEMMA = \"" + this.term_string_edit(lemma) + "\" LEMMA_FREQUENCY =" + str(lemma_freq))
        if (head_term.isDefined) {
          this.outstream.write(" HEAD_TERM = \"" + this.term_string_edit(head_term.get) + "\"")
        }
        if (head_lemma.isDefined) {
          this.outstream.write(" HEAD_LEMMA = \"" + this.term_string_edit(head_lemma.get) + "\"")
        }
        if (term_type.isDefined and (not (term_type.get == "url") )) {
          this.outstream.write(" TERM_PATTERN_TYPE = \"" + term_type + "\"")
        }
        this.outstream.write(os.linesep)
      }
    }

    //
    //
    //
    def __write_term_becomes_article_citation(term: str, instances: List[Tuple[int, int]]): Unit = {
      // global term_id_number @semanticbeeng @global state
      for ((start, end) ← instances) {
        this.term_id_number = 1 + this.term_id_number
        this.outstream.write("CITATION ID = \"NYU_ID_" + str(this.term_id_number) +
                             "\" STRING = \"" + term + "\" CITE_CLASS = \"article\"")
        this.outstream.write(" START = " + str(start) + " END = " + str(end) + os.linesep)
      }
    }

    //
    //
    //
    def __write_term_becomes_organization(term: str, instances: List[Tuple[int, int]]): Unit = {
      // global term_id_number @semanticbeeng @global state
      for ((start, end) ← instances) {
        this.term_id_number = 1 + this.term_id_number
        this.outstream.write("ORGANIZATION ID = \"NYU_ID_" + str(this.term_id_number) + "\" STRING = \"" + term + "\"")
        this.outstream.write(" START =" + str(start) + " END =" + str(end) + os.linesep)
      }
    }

    //
    //   @semanticbeeng ! used
    //
    def write_term_becomes_gpe(term: str, instances: List[Tuple[int, int]]): Unit = {
      // global term_id_number @semanticbeeng @global state
      for ((start, end) ← instances) {
        this.term_id_number = 1 + this.term_id_number
        this.outstream.write("GPE ID = \"NYU_ID_" + str(this.term_id_number) + "\" STRING = \"" + term + '"')
        this.outstream.write(" START =" + str(start) + " END =" + str(end) + os.linesep)
      }
    }

    //
    //
    //
    def __write_term_becomes_person(term: str, instances: List[Tuple[int, int]]): Unit = {
      // global term_id_number @semanticbeeng @global state
      for ((start, end) ← instances) {
        this.term_id_number = 1 + this.term_id_number
        this.outstream.write("PERSON ID = \"NYU_ID_" + str(this.term_id_number) + "\" STRING = \"" + term + "\"")
        this.outstream.write(" START =" + str(start) + " END =" + str(end) + os.linesep)
      }
    }

    //
    //
    //
    // @staticmethod
    def term_string_edit(instring: str): str = {
      val output = re.sub(">", "&gt", instring)
      return (output)
    }

    //
    //
    //
    // @staticmethod
    def org_head_ending(term: str, head_hash: Dict[str, str]): bool = {
      if ((term in head_hash) and term_utilities.org_ending_pattern.search(head_hash(term)))
        return (True)
      return (False)
    }
  }
}