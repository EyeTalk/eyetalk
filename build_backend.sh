#!/usr/bin/env bash

cp backend/keras.json ~

cd backend/eyefinder_cpp
./run_script.sh

cd
mkdir -p .keras
mv keras.json .keras
