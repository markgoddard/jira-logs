#!/usr/bin/env python3

import argparse
import csv
import datetime
import json
import subprocess
import sys


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
        dt = datetime.datetime.strptime(date + " " + start, "%Y-%m-%d %I:%M:%S %p")
        return dt.isoformat() + ".000+0000"

    @staticmethod
    def _parse_duration(duration):
        # Jira requires duration in minutes.
        # I'm sure there's a better way...
        t1 = datetime.datetime.strptime(duration, "%H:%M:%S")
        t0 = datetime.datetime(t1.year, t1.month, t1.day)
        delta = t1 - t0
        return int(delta.total_seconds() / 60)

    def display(self):
        print(f"{self.task} {self.duration_m}m @ {self.start}: {self.comment}")

    def submit(self):
        cmd = f"./jira-log.sh -i {self.task} -t {self.duration_m} -c \"{self.comment}\" -s \"{self.start}\""
        try:
            output = subprocess.check_output(cmd, shell=True,
                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"{e.cmd} exited {e.returncode} stdout: {e.output} stderr: {e.stderr}")
            raise

        output = json.loads(output)
        if "errors" in output or "errorMessages" in output:
            raise Exception(f"Failed to submit work log: {output}")
        elif "self" in output:
            print(f"{output['self']}")
        else:
            raise Exception("Unable to parse response from Jira: {output}")


def _get_logs():
    with open('jira-logs.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            task, duration, comment, date, start = tuple(row)
            log = WorkLog(task, duration, comment, date, start)
            yield log


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--dry-run", action="store_true")
    return parser.parse_args()


def main():
    args = _parse_args()
    for log in _get_logs():
        log.display()
        if not args.dry_run:
            log.submit()


if __name__ == "__main__":
    main()
