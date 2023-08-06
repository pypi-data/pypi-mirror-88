#!/bin/bash


# Ensure that all source code files have the copyright header
set -u


if [ "$#" -eq 0 ]; then
    echo "No files given!"
    exit 0
fi

FAILED=""
for FILE in "$@"; do
    if [ ! -f "$FILE" ]; then
        # File was deleted or renamed.
        continue;
    fi

    if [ ! -s "$FILE" ]; then
        # File is empty
        continue
    fi

    # Check 2nd till 4th lines.
    # 2nd --> cpp, hpp, h
    # 3rd --> py
    # 4th --> py with specified encoding
    sed -n '2,4p' "${FILE}" | grep -z -E '[*|#] AMZ Driverless Project' > /dev/null
    RESULT="$?"

    # Ensure 4th line is correct
    sed -n '4,6p' "${FILE}" | grep -z -E '[*|#] Copyright \(c\) 20.. Authors:' > /dev/null
    RESULT="$?:${RESULT}"
    if [ "${RESULT}" != "0:0" ]; then
        FAILED=$(echo "${FAILED}" ; echo "${FILE}")
    fi
done

if [ ! -z "${FAILED}" ]; then
    echo "The following files are missing copyright headers:"
    echo "${FAILED}"
    exit 1
else
    echo "All files have copyright headers."
    exit 0
fi