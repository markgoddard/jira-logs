#!/usr/bin/env python3

import argparse
import csv
import datetime
import json
import re
import subprocess
import sys
import logging
import os

# Check if the 'output' file exists in the current directory
if os.path.exists('output.log'):
    # Rename the existing 'output' file to 'output-old'
    os.rename('output.log', 'output-old.log')

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)

#log to file 
fh = logging.FileHandler(r'output.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

class WorkLog(object):

    def __init__(self, task, duration, comment, date, start):
        if not task:
            raise Exception("No task provided")
        self.task = task
        self.duration_m = self._parse_duration(duration)
        self.comment = comment
        self.start = self._parse_start(date, start)

    @staticmethod
    def _parse_start(date, start):
        # Jira requires the following format:
        # yyyy-MM-dd'T'HH:mm:ss.SSSZ
        # Convert start to timedelta
        dt = datetime.datetime.strptime(start, "%I:%M:%S %p")
        delta = dt - datetime.datetime(dt.year, dt.month, dt.day)
        # Add to date
        date += delta
        return date.isoformat() + ".000+0000"

    @staticmethod
    def _parse_duration(duration):
        # Jira requires duration in minutes.
        # I'm sure there's a better way...
        t1 = datetime.datetime.strptime(duration, "%H:%M:%S")
        t0 = datetime.datetime(t1.year, t1.month, t1.day)
        delta = t1 - t0
        return int(delta.total_seconds() / 60)

    def display(self):
        yellow = "\x1b[33;20m"
        reset = "\x1b[0m"
        logging.info(f"{yellow}{self.task} {self.duration_m}m @ {self.start}: {self.comment}{reset}")

    def submit(self):
        cmd = f"./jira-log.sh -i {self.task} -t {self.duration_m} -c \"{self.comment}\" -s \"{self.start}\""
        try:
            output = subprocess.check_output(cmd, shell=True,
                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            logging.error(f"{e.cmd} exited {e.returncode} stdout: {e.output} stderr: {e.stderr}")
            raise

        output = json.loads(output)
        if "errors" in output or "errorMessages" in output:
            raise Exception(f"Failed to submit work log: {output}")
        elif "self" in output:
            logging.info(f"{output['self']}")
        else:
            raise Exception("Unable to parse response from Jira: {output}")


def _skip_row(row):
    def non_zero_duration(value):
        # Ignore lines with only a zero duration
        return value != '0:00:00'

    return (not row or
            not any(filter(non_zero_duration, row)) or
            row[0].startswith('#') or
            row[0] == 'Total')


def _get_logs(input_filename, year):
    day = None
    date = None
    # Format: day/month
    date_pattern = re.compile(r"([\d]+)/([\d]+)")
    now = datetime.datetime.now()
    with open(input_filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            logging.info(row)
            if _skip_row(row):
                continue
            if row[1] == "Start":
                day = row[0].strip()
                if not day:
                    raise Exception(f"Unable to find day: {row}")
                groups = date_pattern.match(day).groups()
                day = int(groups[0])
                month = int(groups[1])
                date = datetime.datetime(year, month, day)
                logging.info(f"Setting date to {date}")
                continue

            if not date:
                raise Exception("Expected day")
            empty, start, _, duration, comment, task = tuple(row[:6])
            if task == "ignore":
                continue
            log = WorkLog(task, duration, comment, date, start)
            yield log


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="jira-logs.csv", help="Input CSV file")
    parser.add_argument("-y", "--year", type=int, default=datetime.date.today().year)
    parser.add_argument("-n", "--dry-run", action="store_true")
    return parser.parse_args()


def main():
    args = _parse_args()

    # Validate all logs first
    for log in _get_logs(args.input, args.year):
        pass

    # Submit
    for log in _get_logs(args.input, args.year):
        log.display()
        if not args.dry_run:
            log.submit()


if __name__ == "__main__":
    main()
