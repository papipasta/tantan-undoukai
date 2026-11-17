#!/bin/bash
# 日英 × 8サイズ、1サイズずつ（同時2本）
H=$1; cd "$(dirname "$0")"
for L in ja en; do
  for S in 320x568 360x740 393x852 412x915 568x320 740x360 852x393 1280x720; do
    timeout 200 python3 shot.py $H out_$L $L $S > log_${L}_$S.txt 2>&1 &
    while [ $(jobs -r | wc -l) -ge 2 ]; do sleep 2; done
  done
done; wait; echo DONE > done.flag
