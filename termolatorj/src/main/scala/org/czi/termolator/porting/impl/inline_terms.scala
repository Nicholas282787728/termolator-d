package org.czi.termolator.porting.impl

import org.czi.termolator.porting.DataDef.{FACT, POS, TERMS, str}
import org.czi.termolator.porting.{File, inline_terms_lemmer, inline_terms_writer}
import org.czi.termolator.porting.DataDef._

/**
  * 
  */
object inline_terms extends org.czi.termolator.porting.inline_terms_intf {

  /**
    * 
    */
  override def find_inline_terms(lines : List[str],
                        fact_file : File[FACT],
                        pos_file : File[POS],
                        terms_file : File[TERMS],
                        marked_paragraphs : bool = False,
                        filter_off : bool = False) : Unit = {
                        
      //super.find_inline_terms(lines , fact_file, pos_file, terms_file, marked_paragraphs, filter_off)
      
      pos_offset_table.clear()                // @semanticbeeng @todo @global state mutation initialization
  
      val line_break_match = os.linesep + "(([ \\t]*)[^A-Z \\t])"
      val start_ends: ListM[Tuple[int, int]] = list()
      val txt_strings: ListM[PosFact] = list()
  
      val structure_pattern: Pattern = re.compile("STRUCTURE *TYPE=\"TEXT\" *START=([0-9]*) *END=([0-9]*)", re.I)
      if (os.path.isfile(pos_file.name))
          load_pos_offset_table(pos_file)
      else
          // @semanticbeeng should this not be a fata fault?
          print("Warning POS file does not exist:", pos_file)
  
      // @semanticbeeng @todo @data check of PosFact
      // @semanticbeeng @todo @jep
      // with fact_file.openText() as instream:
      val instream = fact_file.openText()

      import collection.JavaConverters._
      for (line ← instream.readlines().asScala) {
          val _match: Match = structure_pattern.searchM(line)
          if (isDefined(_match)) {
              val start = int(_match.group(1))
              val end = int(_match.group(2))
              start_ends.append((start, end))     // @semanticbeeng @todo static typic
          }
      }

      start_ends.sort()
  
      if ((len(start_ends) > 1) and (not (marked_paragraphs)))
          marked_paragraphs = True
      else
          marked_paragraphs = False
  
      var big_txt: str = ""
  
      if (marked_paragraphs)
          for (line ← lines)
              big_txt = big_txt + re.sub(os.linesep, " ", line)
  
          for ((start, end) ← start_ends)
              txt_strings.append(PosFact(start, end, big_txt.slice(start, end)))
      else {
          val (start, end) = start_ends._1
          val end = 0
          val current_block: str = ""
          var so_far = start
  
          for (line ← lines) {
              val end = so_far + len(line)
              val next_line: str = re.sub(os.linesep, " ", line)
              val current_block = current_block + next_line
              val big_txt = big_txt + next_line
  
              if (not re.search('[a-zA-z]', line)) or re.search('[.?:!][ \t' + os.linesep + ']*$', line) {
                  txt_strings.append(PosFact(start, end, current_block))
                  current_block = ""
                  start = end
              }
              so_far = end
          }
          if (current_block != "")
              txt_strings.append(PosFact(start, end, current_block))
      }

      val termLemmer = new inline_terms_lemmer.TermsLemmer(Abbreviate.abbr_to_full_dict)
  
      for ((start, end, text) ← txt_strings) {
          val text = re.sub(line_break_match, " \g<1>", text)
          var term_tuples : List[Tuple4[int, int, str, str]]

          if ((text.count("\t") + text.count(" ")) < (len(text) / 3)) {
              ////  ignore tables
  
              // @semanticbeeng @todo static typic
              val term_triples: List[Tuple3[int, int, str]] = get_topic_terms(text, start, filter_off=filter_off)  // @todo is this PosFact? or Term
  
              val formulaic_tuples: List[Tuple4[int, int, str, str]] = get_formulaic_term_pieces(text, start)
  
              term_tuples = merge_formulaic_and_regular_term_tuples(term_triples, formulaic_tuples)
          }
          else
              term_tuples = list()

          termLemmer.process_line(term_tuples, big_txt)
      }

      val term_list: List[str] = list(termLemmer.term_hash.keys())
      term_list.sort()

      global_formula_filter(term_list, termLemmer.term_hash.toList, termLemmer.term_type_hash)
  
      // @semanticbeeng @todo @jep
      // with terms_file.openText(mode='w') as outstream:
      val outstream = terms_file.openText("w")
  
      val termWriter = new inline_terms_writer.TermsWriter(outstream)
      termWriter.write_all(term_list, termLemmer)
  
      del (termLemmer)
      del (termWriter)
    }


}
