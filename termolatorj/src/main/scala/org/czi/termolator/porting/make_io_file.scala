package org.czi.termolator.porting

/**
  * Created by nickdsc on 7/12/17.
  */
object make_io_file {

  import DataDef._
  import run_termolator._

  /**
    * nyu-english-new/run_termolator.sh:30
    */
  def main_internal_prefix_list(files : File[File[TXT]], fileTypes : String*)
    : File[File[BARE]] = internal_prefix_list

  def main_internal_pos_list(files : File[File[TXT]], fileTypes : String*)
    : File[File[POS]] = internal_pos_list

  def main_internal_txt_fact_list(files : File[File[TXT]], fileTypes : String*)
    : File[(File[TXT3], File[FACT])] = internal_txt_fact_list

  def main_internal_fact_pos_list(files : File[File[TXT]], fileTypes : String*)
    : File[(File[FACT], File[POS ])] = internal_fact_pos_list

  def main_internal_txt_fact_pos_list(files : File[File[TXT]], fileTypes : String*)
    : File[(File[TXT2], File[FACT], File[POS ])] = internal_txt_fact_pos_list

  def main_internal_pos_terms_abbr_list(files : File[File[TXT]], fileTypes : String*)
    : File[(File[POS], File[TERMS], File[ABBR])] = internal_pos_terms_abbr_list

  def main_internal_foreground_tchunk_list(files : File[File[TXT]], fileTypes : String*)
    : File[File[TCHUNK]] =  internal_foreground_tchunk_list

  def main_internal_background_tchunk_list(files : File[File[TXT]], fileTypes : String*)
    : File[File[TCHUNK]] = internal_background_tchunk_list

}
