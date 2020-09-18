#!/bin/sh

~/mosesdecoder/scripts/training/train-model.perl -root-dir train \
-corpus europarl-v7.de-en.clean -f de -e en \
-alignment grow-diag-final-and -reordering msd-bidirectional-fe \
-lm 0:3:$PWD/news-commentary-v8.fr-en.blm.en:8 \
-external-bin-dir ~/proj4/q3/mosesdecoder/tools \
--first-step 1 --last-step 4
