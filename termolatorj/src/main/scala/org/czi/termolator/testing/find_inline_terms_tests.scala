package org.czi.termolator.testing

import org.czi.termolator.porting.DataDef._
import org.czi.termolator.porting._

import scala.collection.immutable.Seq


/**
  *
  */
object find_inline_terms_tests extends App {

  import DataSet._

  dictionary.ensureModuleInitialized()
  term_utilities.ensureModuleInitialized()
  abbreviate.ensureModuleInitialized()
  find_terms.ensureModuleInitialized()

  // dictionary.read_in_nom_dict()
  // dictionary.read_in_noun_morph_file()
  dictionary.initialize_utilities()

  test_nom_class()

  test_topic_term_ok_boolean()

  test_get_topic_terms()

  allFiles foreach { fileName ⇒
    test_get_topic_terms(fileName)
    test_find_inline_terms_for(fileName)
  }


  /**
    *
    */
  def test_get_topic_terms(fileName : String) = {

    val infile = new File[TXT](fileName+ ".txt")
    val txt2_file = new File[TXT2](fileName+ ".txt2")

    make_termolator_fact_txt_files.create_termolotator_fact_txt_files(
      input_file = infile,
      txt2_file,
      txt3_file = new File[TXT3](fileName + ".txt3"),
      fact_file = new File[FACT](fileName + ".fact"))

    val fact = new File[FACT](fileName + ".fact")
    val pos = new File[FACT](fileName + ".pos")
    run_adjust_missing_char_pos.fix_bad_char_in_file(
      fact,
      pos)

    run_adjust_missing_char_pos.fix_bad_char_in_file(fact, pos)

    val lines: Seq[str] = term_utilities.get_lines_from_file(txt2_file)

    //val text = lines.mkString("")
    val text = "Clinical practice guideline: hoarseness (dysphonia) This guideline provides evidence-based recommendations on managing hoarseness (dysphonia), defined as a disorder characterized by altered vocal quality, pitch, loudness, or vocal effort that impairs communication or reduces voice-related quality of life (QOL). Hoarseness affects nearly one-third of the population at some point in their lives. This guideline applies to all age groups evaluated in a setting where hoarseness would be identified or managed. It is intended for all clinicians who are likely to diagnose and manage patients with hoarseness. The primary purpose of this guideline is to improve diagnostic accuracy for hoarseness (dysphonia), reduce inappropriate antibiotic use, reduce inappropriate steroid use, reduce inappropriate use of anti-reflux medications, reduce inappropriate use of radiographic imaging, and promote appropriate use of laryngoscopy, voice therapy, and surgery. In creating this guideline the American Academy of Otolaryngology-Head and Neck Surgery Foundation selected a panel representing the fields of neurology, speech-language pathology, professional voice teaching, family medicine, pulmonology, geriatric medicine, nursing, internal medicine, otolaryngology-head and neck surgery, pediatrics, and consumers. The panel made strong recommendations that 1) the clinician should not routinely prescribe antibiotics to treat hoarseness and 2) the clinician should advocate voice therapy for patients diagnosed with hoarseness that reduces voice-related QOL. The panel made recommendations that 1) the clinician should diagnose hoarseness (dysphonia) in a patient with altered voice quality, pitch, loudness, or vocal effort that impairs communication or reduces voice-related QOL; 2) the clinician should assess the patient with hoarseness by history and/or physical examination for factors that modify management, such as one or more of the following: recent surgical procedures involving the neck or affecting the recurrent laryngeal nerve, recent endotracheal intubation, radiation treatment to the neck, a history of tobacco abuse, and occupation as a singer or vocal performer; 3) the clinician should visualize the patient's larynx, or refer the patient to a clinician who can visualize the larynx, when hoarseness fails to resolve by a maximum of three months after onset, or irrespective of duration if a serious underlying cause is suspected; 4) the clinician should not obtain computed tomography or magnetic resonance imaging of the patient with a primary complaint of hoarseness prior to visualizing the larynx; 5) the clinician should not prescribe anti-reflux medications for patients with hoarseness without signs or symptoms of gastroesophageal reflux disease; 6) the clinician should not routinely prescribe oral corticosteroids to treat hoarseness; 7) the clinician should visualize the larynx before prescribing voice therapy and document/communicate the results to the speech-language pathologist; and 8) the clinician should prescribe, or refer the patient to a clinician who can prescribe, botulinum toxin injections for the treatment of hoarseness caused by adductor spasmodic dysphonia. The panel offered as options that 1) the clinician may perform laryngoscopy at any time in a patient with hoarseness, or may refer the patient to a clinician who can visualize the larynx; 2) the clinician may prescribe anti-reflux medication for patients with hoarseness and signs of chronic laryngitis; and 3) the clinician may educate/counsel patients with hoarseness about control/preventive measures. This clinical practice guideline is not intended as a sole source of guidance in managing hoarseness (dysphonia). Rather, it is designed to assist clinicians by providing an evidence-based framework for decision-making strategies. The guideline is not intended to replace clinical judgment or establish a protocol for all individuals with this condition, and may not provide the only appropriate approach to diagnosing and managing this problem. "
    val result = inline_terms.get_topic_terms(text, offset = 0, filter_off = False)

    println("Result = ")
    result foreach println
  }

  /**
    *
    */
  def test_find_inline_terms_for(fileName : String) = {

    /**
      * @todo cannot assert anything about this becuase it is monolithical
      */
    find_terms.find_inline_terms_for(fileName, start = true)
  }

  /**
    *
    */
  def test_get_topic_terms() = {

    val text = "Biomechanical Evaluation of Scaphoid and Lunate Kinematics Following Selective Sectioning of Portions of the Scapholunate Interosseous Ligament To determine the relative roles of the dorsal and volar portions of the scapholunate interosseous ligament (SLIL) in the stability of the scaphoid and lunate. Sixteen fresh cadaver wrists were moved through physiological motions using a wrist joint simulator. Electromagnetic sensors measured the motion of the scaphoid and lunate. Data were collected with the wrist intact, after randomly sectioning the dorsal SLIL first (8 wrists) or the volar SLIL first (8 wrists), and after full ligamentous sectioning. Differences in the percent increase in scaphoid flexion or lunate extension were compared using a t test with significance set at P   .05. Sectioning the dorsal SLIL accounted for 37%, 72%, and 68% of the increase in scaphoid flexion in wrist flexion-extension, radioulnar deviation, and dart throw motion as compared with complete SLIL sectioning. Sectioning the volar SLIL accounted for only 7%, 6%, and 14%, respectively. In the same 3 motions, sectioning the dorsal SLIL accounted for 55%, 57%, and 58% of the increase in lunate extension, whereas volar SLIL sectioning accounted for 27%, 28%, and 22%. The dorsal SLIL provides more stability to the scaphoid and lunate in biomechanical testing. The volar SLIL does provide some, although less, stability. Although this study supports the critical importance of dorsal SLIL repairs or reconstructions, it also shows that there may be some value in implementing a volar SLIL repair or reconstruction. "
    val offset = 0
    val filter_off = False
    val out = Array(
      (216, 250, "scapholunate interosseous ligament"),
      (252, 256, "SLIL"),
      (0, 24, "Biomechanical Evaluation"),
      (28, 36, "Scaphoid"),
      (41, 58, "Lunate Kinematics"),
      (69, 89, "Selective Sectioning"),
      (109, 143, "Scapholunate Interosseous Ligament"),
      (161, 175, "relative roles"),
      (183, 189, "dorsal"),
      (194, 208, "volar portions"),
      (216, 250, "scapholunate interosseous ligament"),
      (282, 290, "scaphoid"),
      (295, 301, "lunate"),
      (351, 372, "physiological motions"),
      (404, 427, "Electromagnetic sensors"),
      (455, 463, "scaphoid"),
      (468, 474, "lunate"),
      (549, 560, "dorsal SLIL"),
      (585, 595, "volar SLIL"),
      (629, 651, "ligamentous sectioning"),
      (692, 708, "scaphoid flexion"),
      (712, 728, "lunate extension"),
      (751, 757, "t test"),
      (763, 775, "significance"),
      (807, 818, "dorsal SLIL"),
      (870, 886, "scaphoid flexion"),
      (890, 913, "wrist flexion-extension"),
      (915, 935, "radioulnar deviation"),
      (985, 1000, "SLIL sectioning"),
      (1017, 1027, "volar SLIL"),
      (1116, 1127, "dorsal SLIL"),
      (1179, 1195, "lunate extension"),
      (1205, 1215, "volar SLIL"),
      (1264, 1275, "dorsal SLIL"),
      (1307, 1315, "scaphoid"),
      (1320, 1326, "lunate"),
      (1330, 1351, "biomechanical testing"),
      (1357, 1367, "volar SLIL"),
      (1446, 1465, "critical importance"),
      (1469, 1488, "dorsal SLIL repairs"),
      (1492, 1507, "reconstructions"),
      (1570, 1587, "volar SLIL repair"),
      (1591, 1605, "reconstruction")
    )
    val result = inline_terms.get_topic_terms(text, offset, filter_off)

    val diff = result.diff(out)

    if (diff.nonEmpty) {
      println("Result different than expected")
      diff foreach println
    }
  }


  /**
    *
    */
  def test_topic_term_ok_boolean() = {

    {
      val word_list = List("proximal interphalangeal")
      val pos_list = List("NOUN_OOV")
      val term_string = "proximal interphalangeal"
      val return1 = true

      val result = inline_terms.topic_term_ok_boolean(word_list, pos_list, term_string)

      assert(result == return1)
    }

    {
      val word_list = List("average")
      val pos_list = List("NOUN")
      val term_string = "average"
      val return1 = false
      val result =  inline_terms.topic_term_ok_boolean(word_list, pos_list, term_string)

       assert(result == return1)
    }
  }

  def test_nom_class() = {

    val  word =  "average"
    val pos = "NOUN"
    val return1 = 2

    val result = term_utilities.nom_class(word, pos)

    assert(result == return1)
  }

  def test_term_lemmer = {
    val lemmer = new inline_terms_lemmer.TermsLemmer(null)
  }
}
