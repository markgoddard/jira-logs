#!/usr/bin/env python3

import csv
import subprocess

with open('jira-logs.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[0].startswith('#'):
            continue
        task, duration, comment, date, start = tuple(row)
        start += ":00.000+0000"
        print(f"{task} {duration}m on {date} @ {start}: {comment}")
        subprocess.check_call(
            f"./jira-log.sh -i {task} -t {duration} -c \"{comment}\" -s \"{date}T{start}\"", shell=True)
