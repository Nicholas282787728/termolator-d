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

rm -rf $files_abbr
rm -rf $files_fact
rm -rf $files_pos
rm -rf $files_terms
rm -rf $files_txt2
rm -rf $files_txt3
rm -rf $files_tchunk
rm -rf $files_tchunk_nps


# cleanup intermediate data
rm `find . -name *.abbr`
rm `find . -name *.fact`
rm `find . -name *.pos`
rm `find . -name *.tchunk`
rm `find . -name *.tchunk.nps`
rm `find . -name *.terms`
rm `find . -name *.txt2`
rm `find . -name *.txt3`

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

