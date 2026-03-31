#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 file1.cpp file2.h ..."
  echo "Error: No files provided."
  exit 1
fi

source_files=""
for file in "$@"; do
  source_files+="/project/$file "
done

docker run --rm \
  -v .:/project \
  xianpengshen/clang-tools:21 \
  clang-tidy \
  --config-file=/project/scripts/.clang-tidy \
  -p /project/build \
  $source_files