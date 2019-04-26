#!/usr/bin/env bash

# How to test

## 1. Go to Skiapoden website
firefox https://skiapoden.herokuapp.com/ &

## 2. Send test data
curl -X POST https://skiapoden.herokuapp.com/csv --data-binary @tests.csv > results.csv
sleep 2

## 3. View result
./bin/exel results.csv
