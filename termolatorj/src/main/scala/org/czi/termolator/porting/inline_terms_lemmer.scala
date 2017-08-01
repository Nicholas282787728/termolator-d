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


object inline_terms_lemmer {

  class TermsLemmer {

    object Patterns {
      val compound_inbetween_string: Pattern = re.compile("^ +(of|for) +((the|a|[A-Z]\\.) +)?$", re.I)
    }

    val lemma_dict: Dict[str, str] = Map()
    val lemma_count: Dict[str, int] = Map()
    val term_hash: Dict[str, List[Tuple[int, int]]] = Map()
    val term_type_hash: Dict[str, str] = Map()
    val head_hash: Dict[str, str] = Map()
    // @semanticbeeng @global state  assert that this will ! change from the time of construction;
    var _abbr_to_full_dict: Dict[str, List[str]] = null


    def this(abbr_to_full_dict: Dict[str, List[str]]) = {
      //    this.lemma_dict = Map()
      //    this.lemma_count = Map()
      //    this.term_hash = Map()
      //    this.term_type_hash = Map()
      //    this.head_hash Map()
      // @semanticbeeng @global state  assert that this will ! change from the time of construction;
      this._abbr_to_full_dict = dictionary.freeze_dict (abbr_to_full_dict)
    }

  //    //;
  //    //;
  //    //;
  //    public void process_line
  //    {
  //                     term_tuples List[Tuple[int, int, str, str]],;
  //                     big_txt str);
  //            }
  //        }
  //    }
  //        // compound_tuples = []              // @semanticbeeng @todo ! used;
  //        last_tuple Tuple[int, int, str, str] = None        // @semanticbeeng @todo static typing  @data what is this;
  //        // unit testing System.out.println\("find_inline_terms >> ");
  //        for t_start, t_end, term, term_type in term_tuples;
  //        {
  //            // unit testing;
  //            // System.out.println\("find_inline_terms >> tuple(" + str(t_start) + ", " + str(t_end) + ", " + term + ", " + term_type + ")");
  //            //// for now we will limit compounding ! to function &;
  //            //// lemmas ! to merge entries unless term_type ==;
  //            //// 'chunk-based';
  //if (  term in this.term_hash )
  //            {
  //                this.term_hash[term].append((t_start, t_end))                            // @semanticbeeng @todo static typing;
  //                lemma = this.get_term_lemma(term, term_type=term_type);
  //if (  lemma in this.lemma_count )
  //                {
  //                    this.lemma_count[lemma] = this.lemma_count[lemma] + 1;
  //    }
  //                else;
  //                {
  //                    this.lemma_count[lemma] = 1;
  //        }
  //    }
  //            else;
  //            {
  //                this.term_hash[term] = [(t_start, t_end)]                                // @semanticbeeng @todo static typing;
  //                this.term_type_hash[term] = term_type;
  //                lemma = this.get_term_lemma(term, term_type=term_type);
  //if (  lemma in this.lemma_count )
  //                {
  //                    this.lemma_count[lemma] = this.lemma_count[lemma] + 1;
  //    }
  //                else;
  //                {
  //                    this.lemma_count[lemma] = 1;
  //        }
  //    }
  //if (  last_tuple & (t_start > last_tuple[1]) & (last_tuple[3] in [false, 'chunk-based']) & (term_type in [false, 'chunk-based']) )
  //            {
  //                inbetween = this.Patterns.compound_inbetween_string.search(big_txt[last_tuple[1]t_start]);
  //if (  inbetween )
  //                {
  //                    compound_term str = term_utilities.interior_white_space_trim(big_txt[last_tuple[0]t_end]);
  //                    //// compound_term = re.sub('\s+',' ',big_txt[last_tuple[0]t_end]);
  //                    compound_tuple Tuple[int, int, str, str] = (last_tuple[0], t_end, compound_term, 'chunk-based')        // @semanticbeeng @todo static typing @data ??;
  //                    //// term_tuples.append(compound_tuple);
  //if (  compound_term in this.term_hash )
  //                    {
  //                        this.term_hash[compound_term].append((last_tuple[0], t_end))     // @semanticbeeng @todo static typing;
  //                        lemma = this.get_compound_lemma(compound_term, last_tuple[2], term);
  //if (  lemma in this.lemma_count )
  //                        {
  //                            this.lemma_count[lemma] = this.lemma_count[lemma] + 1;
  //    }
  //                        else;
  //                        {
  //                            this.lemma_count[lemma] = 1;
  //        }
  //    }
  //                    else;
  //                    {
  //                        this.term_hash[compound_term] = [(last_tuple[0], t_end)]           // @semanticbeeng @todo static typing;
  //                        this.head_hash[compound_term] = last_tuple[2];
  //                        lemma = this.get_compound_lemma(compound_term, last_tuple[2], term);
  //if (  lemma in this.lemma_count )
  //                        {
  //                            this.lemma_count[lemma] = this.lemma_count[lemma] + 1;
  //    }
  //                        else;
  //                        {
  //                            this.lemma_count[lemma] = 1;
  //        }
  //    }
  //                    last_tuple = compound_tuple[];
  //    }
  //if (  ! re.search('[^\s]', big_txt[last_tuple[1]t_start]) )
  //                {
  //                    compound_term = term_utilities.interior_white_space_trim(big_txt[last_tuple[0]t_end]);
  //                    compound_tuple = (last_tuple[0], t_end, compound_term, 'chunk-based')   //  @semanticbeeng @todo static typing;
  //if (  compound_term in this.term_hash )
  //                    {
  //                        this.term_hash[compound_term].append((last_tuple[0], t_end))     //  @semanticbeeng @todo static typing;
  //                        lemma = this.get_compound_lemma(compound_term, last_tuple[2], term);
  //if (  lemma in this.lemma_count )
  //                        {
  //                            this.lemma_count[lemma] = this.lemma_count[lemma] + 1;
  //    }
  //                        else;
  //                        {
  //                            this.lemma_count[lemma] = 1;
  //        }
  //    }
  //                    else;
  //                    {
  //                        this.term_hash[compound_term] = [(last_tuple[0], t_end)]         //  @semanticbeeng @todo static typing;
  //                        //// if there is only blank space & no;
  //                        //// preposition between terms, the;
  //                        //// compounding is normal noun noun;
  //                        //// compounding, rather than the inversion;
  //                        //// used for noun prep noun sequences;
  //                        lemma = this.get_compound_lemma(compound_term, last_tuple[2], term);
  //                        this.head_hash[compound_term] = term;
  //if (  lemma in this.lemma_count )
  //                        {
  //                            this.lemma_count[lemma] = this.lemma_count[lemma] + 1;
  //    }
  //                        else;
  //                        {
  //                            this.lemma_count[lemma] = 1;
  //            }
  //        }
  //    }
  //                else;
  //                {
  //                    last_tuple = (t_start, t_end, term, term_type)      //  @semanticbeeng @todo static typing;
  //        }
  //    }
  //            else;
  //            {
  //                last_tuple = (t_start, t_end, term, term_type)          //  @semanticbeeng @todo static typing;
  //            }
  //        }
  //    }
  //    //;
  //    //  @semanticbeeng @func comp_termChunker;
  //    //  @semanticbeeng @todo static typing;
  //    //;
  //    public void get_term_lemma( term str, term_type str=None) -> str
  //    {
  //        //// add plural --> singular;
  //        //// System.out.println\(term,term_type);
  //        // global lemma_dict;
  //        last_word_pat = re.compile('[a-z]+$', re.I);
  //if (  term in this.lemma_dict )
  //        {
  //            return (this.lemma_dict[term]);
  //    }
  //if (  term_type & (term_type != 'chunk-based') )
  //        {
  //            //// this takes care of all the patterned cases;
  //            output = term.upper();
  //    }
  //        elif (term in this._abbr_to_full_dict) & (len(this._abbr_to_full_dict[term]) > 0) & \;
  //        {
  //                (term.isupper() or (! term in config.pos_dict) or (term in dictionary.jargon_words));
  //    }
  //            output = this._abbr_to_full_dict[term][0];
  //    }
  //        else;
  //        {
  //            last_word_match = last_word_pat.search(term);
  //if (  last_word_match )
  //            {
  //                last_word = last_word_match.group(0).lower();
  //                last_word_start = last_word_match.start();
  //if (  (last_word in dictionary.noun_base_form_dict) & (! last_word.endswith('ing')) )
  //                {
  //if (  (last_word in dictionary.noun_base_form_dict[last_word]) )
  //                    {
  //                        output = term.upper();
  //    }
  //                    else;
  //                    {
  //                        output = (term[last_word_start] + dictionary.noun_base_form_dict[last_word][0]).upper();
  //        }
  //    }
  //if (  last_word.endswith('ies') )
  //                {
  //                    output = (term[-3] + 'y').upper();
  //    }
  //if (  last_word.endswith('es') & (len(last_word) > 3) & (last_word[-3] in 'oshzx') )
  //                {
  //                    output = term[-2].upper();
  //    }
  //if (  last_word.endswith('(s)') )
  //                {
  //                    output = term[-3].upper();
  //    }
  //if (  (len(last_word) > 1) & last_word.endswith('s') & term[-1].isalpha() & (! last_word[-2] in 'u') )
  //                {
  //                    output = term[-1].upper();
  //    }
  //                else;
  //                {
  //                    output = term.upper();
  //        }
  //    }
  //if (  re.search('\([sS]\)$', term) )
  //            {
  //                output = term[-3].upper();
  //    }
  //            else;
  //            {
  //                output = term.upper();
  //        }
  //    }
  //        this.lemma_dict[term] = output           // @semanticbeeng @todo global state mutation;
  //        return (output);
  //    }
    //;
    //;
    //;
    def get_compound_lemma(compound_term: str, first_term: str, second_term: str) : str = {

      if (compound_term in this.lemma_dict) {
        return (this.lemma_dict[compound_term]) // @semanticbeeng @todo global state reference;

      } else {

        val first_lemma = this.get_term_lemma(first_term, term_type = 'chunk - based')
        val second_lemma = this.get_term_lemma(second_term, term_type = 'chunk - based')
        vL output = (second_lemma + ' ' + first_lemma).upper()
        this.lemma_dict[compound_term] = output // @semanticbeeng @todo global state mutation;
        return (output)
      }
    }
  }
}
