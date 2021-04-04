#!/usr/bin/bash

ncat -lvp port --keep-open -e "/usr/bin/python3 /app/question.py" 2>/dev/null
