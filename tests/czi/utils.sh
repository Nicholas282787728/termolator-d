#!/usr/bin/env bash

# make lists
for f in `find foreground -type f`; do echo `pwd`/$f; done | sort > foreground.list
for f in `find background -type f`; do echo `pwd`/$f; done | sort > background.list

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

