package org.czi.termolator.porting

//import re;
//import dictionary;
//import term_utilities;
//from typing import List, Tuple, Dict, Pattern;
//import config;
//;
//   Extracts stats for a a single source "file" & manages the @state derived;
//;
import org.czi.termolator.porting.DataDef._

import scala.collection.mutable

object inline_terms_lemmer {

  class TermsLemmer(abbr_to_full_dict: Dict[str, List[str]]) {

    object Patterns {
      val compound_inbetween_string: Pattern = re.compile("^ +(of|for) +((the|a|[A-Z]\\.) +)?$", re.I)
    }

    val term_hash: Dict[str, ListM[Tuple[int, int]]] = new mutable.HashMap[str, ListM[Tuple[int, int]]]()
    val term_type_hash: Dict[str, str] = new mutable.HashMap[str, str]()

    val head_hash: Dict[str, str] = new mutable.HashMap[str, str]()

    val lemma_dict: Dict[str, str] = new mutable.HashMap[str, str]()
    val lemma_count: Dict[str, int] = new mutable.HashMap[str, int]()

    // @semanticbeeng @global state  assert that this will ! change from the time of construction;
    var _abbr_to_full_dict: Dict[str, List[str]] = _

    // def this(abbr_to_full_dict: Dict[str, List[str]]) = this(dictionary.freeze_dict (abbr_to_full_dict))

    object Patterns {
      val compound_inbetween_string: Pattern = re.compile("^ +(of|for) +((the|a|[A-Z]\.) +)?$", re.I)
    }
    
    // 
    // 
    // 
    def this(abbr_to_full_dict: Dict[str, List[str]]) =
      this(0L, dictionary.freeze_dict(abbr_to_full_dict))
    
    //
    //
    //
    def process_line(term_tuples: List[Tuple4[int, int, str, str]], big_txt: str): Unit = {

        // compound_tuples = []                               // @semanticbeeng @todo not used
        var last_tuple: Tuple4[int, int, str, str] = null        // @semanticbeeng static typing  @data what is this

        // unit testing print("find_inline_terms >> ")
        for ((t_start, t_end, term, term_type) ← term_tuples) {
            // unit testing
            // print("find_inline_terms >> tuple(" + str(t_start) + ", " + str(t_end) + ", " + term + ", " + term_type + ")")

            //// for now we will limit compounding not to function and
            //// lemmas not to merge entries unless term_type ==
            //// 'chunk-based'
            if (term in this.term_hash) {

                this.term_hash(term).append((t_start, t_end))                               // @semanticbeeng static typing
                val lemma = this.get_term_lemma(term, term_type=Some(term_type))

                if (lemma in this.lemma_count)
                    this.lemma_count(lemma) = this.lemma_count(lemma) + 1
                else
                    this.lemma_count(lemma) = 1
            } else {
                this.term_hash(term) = list((t_start, t_end))                                // @semanticbeeng static typing
                this.term_type_hash(term) = term_type

                val lemma = this.get_term_lemma(term, term_type=Some(term_type))

                if (lemma in this.lemma_count)
                    this.lemma_count(lemma) = this.lemma_count(lemma) + 1
                else
                    this.lemma_count(lemma) = 1
            }
            
            if (isDefined(last_tuple) and (t_start > last_tuple._2) 
                        and (last_tuple._4 in List(False, "chunk-based")) and (term_type in List(False, "chunk-based"))) {
                val inbetween = this.Patterns.compound_inbetween_string.search(big_txt.slice(last_tuple._1, t_start))

                if (inbetween) {
                    val compound_term: str = term_utilities.interior_white_space_trim(big_txt.slice(last_tuple._1, t_end))
                    //// compound_term = re.sub("\s+"," ",big_txt[last_tuple[0]:t_end])

                    val compound_tuple: Tuple4[int, int, str, str] = (last_tuple._1, t_end, compound_term, "chunk-based")        // @semanticbeeng static typing @data ??
                    //// term_tuples.append(compound_tuple)

                    if (compound_term in this.term_hash) {
                        this.term_hash(compound_term).append((last_tuple._1, t_end))     // @semanticbeeng static typing
                        val lemma = this.get_compound_lemma(compound_term, last_tuple._3, term)

                        if (lemma in this.lemma_count)
                            this.lemma_count(lemma) = this.lemma_count(lemma) + 1
                        else
                            this.lemma_count(lemma) = 1
                    }
                    else
                        this.term_hash(compound_term) = list((last_tuple._1, t_end))           // @semanticbeeng static typing
                        this.head_hash(compound_term) = last_tuple._3
                        val lemma = this.get_compound_lemma(compound_term, last_tuple._3, term)

                        if (lemma in this.lemma_count)
                            this.lemma_count(lemma) = this.lemma_count(lemma) + 1
                        else
                            this.lemma_count(lemma) = 1
                    last_tuple = compound_tuple //@todo syntax [:]
                }
                else if  (not (re.search("[^\s]", big_txt.slice(last_tuple._2, t_start)))) {
                    val compound_term = term_utilities.interior_white_space_trim(big_txt.slice(last_tuple._1, t_end))

                    val compound_tuple = (last_tuple._1, t_end, compound_term, "chunk-based")   //  @semanticbeeng static typing

                    if (compound_term in this.term_hash) {
                        this.term_hash(compound_term).append((last_tuple._1, t_end))     //  @semanticbeeng static typing
                        val lemma = this.get_compound_lemma(compound_term, last_tuple._3, term)
                        if (lemma in this.lemma_count)
                            this.lemma_count(lemma) = this.lemma_count(lemma) + 1
                        else
                            this.lemma_count(lemma) = 1
                    }
                    else {
                        this.term_hash(compound_term) = list((last_tuple._1, t_end))         //  @semanticbeeng static typing
                        //// if there is only blank space and no
                        //// preposition between terms, the
                        //// compounding is normal noun noun
                        //// compounding, rather than the inversion
                        //// used for noun prep noun sequences
                        val lemma = this.get_compound_lemma(compound_term, last_tuple._3, term)
                        this.head_hash(compound_term) = term
                        if (lemma in this.lemma_count)
                            this.lemma_count(lemma) = this.lemma_count(lemma) + 1
                        else
                            this.lemma_count(lemma) = 1
                     }       
                }     
                else
                    last_tuple = (t_start, t_end, term, term_type)      //  @semanticbeeng static typing
            }
            else
                last_tuple = (t_start, t_end, term, term_type)          //  @semanticbeeng static typing
          }
    }
    
    //
    //  @semanticbeeng @func comp_termChunker
    //  @semanticbeeng static typing
    //
    def get_term_lemma(term: str, term_type: Optional[str] = None) : str = {
        //// add plural --> singular
        //// print(term,term_type)
        // global lemma_dict

        val last_word_pat = re.compile("[a-z]+$", re.I)

        var output : str = null
        if (term in this.lemma_dict)
            return (this.lemma_dict(term))

        else if (isDefined(term_type) and (term_type.get != "chunk-based"))
            //// this takes care of all the patterned cases
            output = term.upper()

        else if ((term in this._abbr_to_full_dict) and (len(this._abbr_to_full_dict(term)) > 0)
            and (term.isupper() or (not (term in config.pos_dict) or (term in dictionary.jargon_words))))
            output = this._abbr_to_full_dict(term)(0)

        else {
            val last_word_match = last_word_pat.search(term)

            if (last_word_match) {
                val last_word: str = last_word_match.group(0).lower()
                val last_word_start: int = last_word_match.start()

                if ((last_word in dictionary.noun_base_form_dict) and (not (last_word.endswith("ing")))) {
                    if (last_word in dictionary.noun_base_form_dict(last_word))
                        output = term.upper()
                    else
                        output = (term.slice(0L, last_word_start) + dictionary.noun_base_form_dict(last_word)(0)).upper()
                }
                else if (last_word.endswith("ies"))
                    output = (term.slice(0, -3) + "y").upper()
                else if (last_word.endswith("es") and (len(last_word) > 3) and (last_word.at(-3) in "oshzx"))
                    output = term.slice(0, -2).upper()
                else if (last_word.endswith("(s)"))
                    output = term.slice(0, -3).upper()
                else if ((len(last_word) > 1) and last_word.endswith("s") and term.at(-1).isalpha() and (not (last_word.at(-2) in "u")))
                    output = term.slice(0, -1).upper()
                else
                    output = term.upper()
            }
            else if (re.search("\([sS]\)$", term))
                output = term.slice(0,-3).upper()
            else
                output = term.upper()
        }
        this.lemma_dict(term) = output           // @semanticbeeng global state mutation
        return (output)
    }

    //
    //
    //
    def get_compound_lemma(compound_term: str, first_term: str, second_term: str) : str = {
        if (compound_term in this.lemma_dict) 
            return (this.lemma_dict(compound_term))     // @semanticbeeng global state reference
        else {
            val first_lemma = this.get_term_lemma(first_term, term_type=Some("chunk-based"))
            val second_lemma = this.get_term_lemma(second_term, term_type=Some("chunk-based"))
            val output = (second_lemma + " " + first_lemma).upper()
            this.lemma_dict(compound_term) = output      // @semanticbeeng global state mutation
            return (output)
        }    
     }
  }
}
