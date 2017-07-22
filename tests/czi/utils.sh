#!/usr/bin/env bash

# make lists
for f in `find foreground -type f`; do echo `pwd`/$f; done | sort > foreground.list
for f in `find background -type f`; do echo `pwd`/$f; done | sort > background.list


# collect intermediate files
files_abbr=`find . -name *.abbr`
files_fact=`find . -name *.fact`
files_pos=`find . -name *.pos`
files_terms=`find . -name *.terms`
files_txt2=`find . -name *.txt2`
files_txt3=`find . -name *.txt3`
files_tchunk=`find . -name *.tchunk`
files_tchunk_nps=`find . -name *.tchunk.nps`

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

# -- manual run
TESTNAME=DAVETEST

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

# $TERMOLATOR/distributional_component.py $4.internal_foreground_tchunk_list $4.internal_background_tchunk_list > $4.all_terms


