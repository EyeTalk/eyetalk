#!/bin/bash

if [ ! -d "build" ]; then
  mkdir -p build && cd build && cmake .. -DUSE_AVX_INSTRUCTIONS=ON && make -j && cd ..
else
  cd build && make -j && cd ..
fi

if [ "$1" == "run" ]; then
  build/eyefinder
fi
