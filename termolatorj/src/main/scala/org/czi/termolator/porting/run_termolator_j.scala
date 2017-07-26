package org.czi.termolator.porting

import scala.language.higherKinds


/**
  * A Scala version of the overall recipe
  *
  * Mapping logic
  * Always with the same names for ease of tracing
  * 1. for every Python file create an object (with the same name)
  * 2. for every function in the file create a method in the object
  * 3. for every function capture inputs, outputs and side effects like file reads and writes
  * 4. for every such data elements used between functions or in files define strong types
  * This is key to ease the comprehension of the overall flow)
  * 5. for every function define the body to capture the function calls (call graph)
  * 6. capture all references to global variables
  */



object run_termolator_j {

  import DataDef._


  /**
    * @code_reference [[./nyu-english-new/run_termolator.sh:27]]
    *
    * ## Step 1: Finding inline terms for foreground files
    * echo "Running Step 1: finding inline terms for foreground files"
    * ## generates fact, txt2 and txt3 files from input files
    */
  val foregroundFiles : File[File[TXT]] = ??? // @todo

  /**
    * "$TESTNAME.internal_prefix_list"
    */
  var internal_prefix_list : File[File[BARE]] =
    make_io_file.main_internal_prefix_list(foregroundFiles, "BARE")

  var internal_pos_list : File[File[POS]]  =
    make_io_file.main_internal_pos_list(foregroundFiles, ".pos")

  var internal_txt_fact_list : File[(File[TXT3], File[FACT])] =
    make_io_file.main_internal_txt_fact_list(foregroundFiles, ".txt3", ".fact")

  var internal_fact_pos_list  : File[(File[FACT], File[POS])] =
    make_io_file.main_internal_fact_pos_list(foregroundFiles, ".fact", ".pos")

  var internal_txt_fact_pos_list : File[(File[TXT2], File[FACT],  File[POS] )] =
    make_io_file.main_internal_txt_fact_pos_list(foregroundFiles, ".txt2", ".fact", ".pos")

  var internal_pos_terms_abbr_list : File[(File[POS],  File[TERMS], File[ABBR])] =
    make_io_file.main_internal_pos_terms_abbr_list(foregroundFiles, ".pos", ".terms", ".abbr")

  var internal_foreground_tchunk_list : File[File[TCHUNK]] =
    make_io_file.main_internal_foreground_tchunk_list(foregroundFiles, ".tchunk")

  val backgroundFiles : File[File[TXT]] = ???  // @todo

  var internal_background_tchunk_list  : File[File[TCHUNK]] =
    make_io_file.main_internal_background_tchunk_list(backgroundFiles, ".tchunk")

  /**
    * Generate the actual context (some of it?)
    */
  val factFiles: Seq[(File[TXT2], File[TXT3], File[FACT])] =
    make_termolator_fact_txt_files.main(internal_prefix_list, ".txt")

  /**
    *
    */
  internal_pos_list = generate_POS(internal_txt_fact_list)

  run_adjust_missing_char_pos.main(internal_fact_pos_list)

  val files: List[(File[FACT], File[POS], File[TERMS])] =
    run_find_inline_terms.main(internal_prefix_list, "DAVETEST", null)

  /**
    * @code_reference [[./nyu-english-new/run_termolator.sh:56]]
    * echo "Chunking for inline term detection"
    */

  internal_foreground_tchunk_list = run_make_term_chunk.main(internal_pos_terms_abbr_list)

  /**
    * ## Step 2 if not already processed, process the backgound files to find all
    * @code_reference [[./nyu-english-new/run_termolator.sh:60]]
    */

  internal_prefix_list = make_io_file.main_internal_prefix_list(backgroundFiles, "BARE")
  internal_pos_list = make_io_file.main_internal_pos_list(backgroundFiles, ".pos")
  internal_txt_fact_list = make_io_file.main_internal_txt_fact_list(backgroundFiles, ".txt3", ".fact")
  internal_fact_pos_list = make_io_file.main_internal_fact_pos_list(backgroundFiles, ".fact", ".pos")
  internal_txt_fact_pos_list = make_io_file.main_internal_txt_fact_pos_list(backgroundFiles, ".txt2", ".fact", ".pos")
  internal_pos_terms_abbr_list = make_io_file.main_internal_pos_terms_abbr_list(backgroundFiles, ".pos", ".terms", ".abbr")

  /**
    * @note no chunking for background files
    */
  //  make_io_file.main_internal_foreground_tchunk_list(foregroundFiles)
  //  make_io_file.main_internal_background_tchunk_list(backgroundFiles)

  /**
    * @note run this again?
    */
  //internal_prefix_list =
    make_termolator_fact_txt_files.main(internal_prefix_list, ".txt")

  /**
    * ## generates fact, txt2 and txt3 files from input files
    * @code_reference [[./run_termolator.sh:70]]
    */
  /**
    * @note this same call is run again with same files but this time for the background files !
    */
  internal_pos_list = generate_POS(internal_txt_fact_list)

  run_adjust_missing_char_pos.main(internal_fact_pos_list)

  /**
    * @code_reference [[./nyu-english-new/run_termolator.sh:75]]
    * @note this is run again for background files
    */
  //val topic_areas = null
  run_find_inline_terms.main(internal_prefix_list, /*output_file_name*/null, null)

  /**
    * @code_reference [[./nyu-english-new/run_termolator.sh:76]]
    * echo "Chunking for inline term detection"
    */

  /**
    * @todo should use [[internal_background_tchunk_list]] instead of [[internal_foreground_tchunk_list]]
    */
  internal_background_tchunk_list = run_make_term_chunk.main(internal_pos_terms_abbr_list)

  /**
    * @code_reference [[./run_termolator.sh:79]]
    *
    *echo "calling distributional_component.py in term_extration using foreground and background tchunk list with output to file $4.all_terms"
    */




  // ============== END ==============
  /**
    * @code_reference [[./nyu-english-new/run_termolator.sh:41]]
    * @todo scaffold
    */
  def generate_POS(input : File[(File[TXT3], File[FACT])] ) : File[File[POS]] = {

    /**
      * @code_reference [[./nyu-english-new/run_termolator.sh:44]]
      * @todo scaffold: this generates files so it will have to be modified for in memory data flow
      *
      * tail -n +2 ${TERMOLATOR}/TERMOLATOR_POS.properties >> temporary_TERMOLATOR_POS.properties
      * echo "Calling Java Consule TJet jar with properties above"
      * java -Xmx16g -cp ${TERMOLATOR}/TJet.jar FuseJet.Utils.Console ./temporary_TERMOLATOR_POS.properties internal_txt_fact_list internal_pos_list
      *
      * ## generates POS files
      */
    FuseJet_Utils_Console.main(input)
    internal_pos_list
  }


}
