#!/bin/bash

#rm frames/*density*.ppm
visit -cli -nowin -s movie_density.py
ls frames/*density*.ppm > frames/file_list
rm *density*.fli
ppm2fli -v -s25 -g460x783 frames/file_list isoSelfG_run.fli
