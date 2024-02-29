#!/bin/sh
while IFS= read -r line
do
  echo "from stdin: $line"
done
