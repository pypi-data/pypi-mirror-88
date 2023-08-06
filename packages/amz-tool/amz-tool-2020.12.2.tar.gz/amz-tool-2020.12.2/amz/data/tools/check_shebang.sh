#!/bin/bash


# Ensure that all source code files have a python shebang line
set -u


if [ "$#" -eq 0 ]; then
    echo "No files given!"
    exit 0
fi

FAILED=""
for FILE in "$@"; do
    if [ ! -f "$FILE" ]; then
        # File was deleted or renamed.
        continue
    fi

    if [ ! -s "$FILE" ]; then
        # File is empty
        continue
    fi
    
    # Ensure 1st line is correct
    sed '1q;d' "${FILE}" | grep -E '#!/usr/bin/env python[2|3]' > /dev/null
    RESULT="$?"

    if [ "${RESULT}" != "0" ]; then
        FAILED=$(echo "${FAILED}" ; echo "${FILE}")
    fi
done

if [ ! -z "${FAILED}" ]; then
    echo "The following files are missing a shebang line clearly indicating the python version:"
    echo "${FAILED}"
    exit 1
else
    echo "All python files have shebang lines."
    exit 0
fi