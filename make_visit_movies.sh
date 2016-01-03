#!/bin/bash

#rm frames/*density*.ppm
mkdir frames
visit -cli -nowin -s density_movie.py
ls frames/*density*.ppm > frames/file_list
rm *density*.fli
ppm2fli -v -s25 -g460x783 frames/file_list isoSelfG_run.fli
