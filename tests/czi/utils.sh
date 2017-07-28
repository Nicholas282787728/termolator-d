#!/usr/bin/env bash

# make lists
for f in `find foreground -name *.txt`; do echo `pwd`/$f; done | sort > foreground.list
for f in `find background -name *.txt`; do echo `pwd`/$f; done | sort > background.list


# collect intermediate files
rootdir=.    # ., foreground or background

files_abbr=`find $rootdir -name *.abbr`
files_fact=`find $rootdir -name *.fact`
files_pos=`find $rootdir -name *.pos`
files_terms=`find $rootdir -name *.terms`
files_txt2=`find $rootdir -name *.txt2`
files_txt3=`find $rootdir -name *.txt3`
files_tchunk=`find $rootdir -name *.tchunk`
files_tchunk_nps=`find $rootdir -name *.tchunk.nps`
files_all="$files_abbr $files_fact $files_pos $files_terms $files_txt2 $files_txt3 $files_tchunk $files_tchunk_nps"

echo $files_abbr        | wc
echo $files_fact        | wc
echo $files_pos         | wc
echo $files_terms       | wc
echo $files_txt2        | wc
echo $files_txt3        | wc
echo $files_tchunk      | wc
echo $files_tchunk_nps  | wc

# cleanup intermediate data
rm -rf $files_abbr
rm -rf $files_fact
rm -rf $files_pos
rm -rf $files_terms
rm -rf $files_txt2
rm -rf $files_txt3
rm -rf $files_tchunk
rm -rf $files_tchunk_nps

cp $files_all /development/projects/04_clients/czi/ds/The_Termolator/tests/czi/lkg_run/intermdata/

# cleanup internal intermediate data
rm false.dict_full_to_abbr
rm false.dict_abbr_to_full
rm .filter.save
rm temporary_TERMOLATOR_POS.properties

rm *.internal_pos_list
rm *.internal_pos_terms_abbr_list
rm *.internal_prefix_list
rm *.internal_background_tchunk_list
rm *.internal_txt_fact_list
rm *.internal_fact_pos_list
rm *.internal_txt_fact_pos_list
rm *.internal_foreground_tchunk_list

rm *.dict_full_to_abbr
rm *.dict_abbr_to_full

rm *.out_term_list
rm *.rejected-terms

rm *.all_terms
rm *.scored_output

# -- manual run ---
# -----------------
TESTNAME=DAVETEST

rm $TESTNAME.*

# Process foreground files
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_prefix_list BARE
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_pos_list .pos
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_txt_fact_list .txt3 .fact
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_fact_pos_list .fact .pos
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_txt_fact_pos_list .txt2 .fact .pos
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_pos_terms_abbr_list .pos .terms .abbr
$TERMOLATOR/make_io_file.py $NYU_DIR/foreground.list $TESTNAME.internal_foreground_tchunk_list .tchunk
$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_background_tchunk_list .tchunk

$TERMOLATOR/make_termolator_fact_txt_files.py $TESTNAME.internal_prefix_list .txt

echo "FuseJet.path1 = ${TERMOLATOR}/models" > temporary_TERMOLATOR_POS.properties
tail -n +2 ${TERMOLATOR}/TERMOLATOR_POS.properties >> temporary_TERMOLATOR_POS.properties

java -Xmx16g -cp ${TERMOLATOR}/lib/TJet.jar FuseJet.Utils.Console ./temporary_TERMOLATOR_POS.properties $TESTNAME.internal_txt_fact_list $TESTNAME.internal_pos_list

$TERMOLATOR/run_adjust_missing_char_pos.py $TESTNAME.internal_fact_pos_list

$TERMOLATOR/run_find_inline_terms.py $TESTNAME.internal_prefix_list $TESTNAME

$TERMOLATOR/run_make_term_chunk.py $TESTNAME.internal_pos_terms_abbr_list $TESTNAME.internal_foreground_tchunk_list

# -----
# Process background files
# -----

$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_prefix_list BARE
$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_pos_list .pos
$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_txt_fact_list .txt3 .fact
$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_fact_pos_list .fact .pos
$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_txt_fact_pos_list .txt2 .fact .pos
$TERMOLATOR/make_io_file.py $NYU_DIR/background.list $TESTNAME.internal_pos_terms_abbr_list .pos .terms .abbr

$TERMOLATOR/make_termolator_fact_txt_files.py $TESTNAME.internal_prefix_list .txt
## generates fact, txt2 and txt3 files from input files

java -Xmx16g -cp ${TERMOLATOR}/lib/TJet.jar FuseJet.Utils.Console ./temporary_TERMOLATOR_POS.properties $TESTNAME.internal_txt_fact_list $TESTNAME.internal_pos_list
## generates POS files

$TERMOLATOR/run_adjust_missing_char_pos.py $TESTNAME.internal_fact_pos_list

$TERMOLATOR/run_find_inline_terms.py $TESTNAME.internal_prefix_list false

$TERMOLATOR/run_make_term_chunk.py $TESTNAME.internal_pos_terms_abbr_list $TESTNAME.internal_background_tchunk_list

echo "calling distributional_component.py in term_extration using foreground and background tchunk list with output to file $TESTNAME.all_terms"

$TERMOLATOR/distributional_component.py $TESTNAME.internal_foreground_tchunk_list $TESTNAME.internal_background_tchunk_list > $TESTNAME.all_terms

#if [ "${12}" = "False" ]; then
   echo "calling filter_term_output.py with $TESTNAME $4.outputweb.score $6 $7 ${10}"
   $TERMOLATOR/filter_term_output.py $TESTNAME $TESTNAME.outputweb.score False 8400
#else
#   echo "calling filter_term_output.py with $4 ${12} $6 $7 ${10}"
#   $TERMOLATOR/filter_term_output.py $4 ${12} $6 $7 ${10}
#fi

echo "Final terms can be found in $4.out_term_list from the scored file in $4.scored_output"
head -1400 $TESTNAME.scored_output | cut -f 1 > $TESTNAME.out_term_list


# ----
# Regresion testing

sort $TESTNAME.all_terms > $TESTNAME.all_terms.sorted
sort $TESTNAME.scored_output > $TESTNAME.scored_output.sorted
