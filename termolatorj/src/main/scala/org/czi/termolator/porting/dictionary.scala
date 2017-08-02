package org.czi.termolator.porting

import org.czi.termolator.porting.DataDef.Dict

import DataDef._

/**
  *
  */
object dictionary extends JepEnabled {

  val moduleName = "dictionary"

  val jargon_words: Set[str] = null// @todo
  val noun_base_form_dict: Dict[str, List[str]] = null

  /**
    *
    */
  def freeze_dict[K, V](d: Dict[K, V]) = d


  /**
    *
    */
  def initialize_utilities() = {
    FunctionDef("initialize_utilities").pyCall()

  }

  /**
    *
    */
  def read_in_noun_morph_file() : Unit = {
    FunctionDef("read_in_noun_morph_file").pyCall()
  }

  /**
    *
    */
  def read_in_nom_dict() : Unit = {
    FunctionDef("read_in_nom_dict").pyCall()
  }
}
