#!/usr/bin/bash

ncat -lvp port -e "/usr/bin/python3 /app/question.py"
