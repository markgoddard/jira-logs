# Jira logs

Script to upload work logs to Jira.

Log entries into a spreadsheet, with the following format:

```
1st	Start		Finish		Duration	Activity	Task
	9:00:00 AM	12:30:00 PM	3:30:00		Morning task	JIRA-123
	13:00:00 PM	17:00:00 PM	4:00:00		Afternoon task	JIRA-456

2nd	Start		Finish		Duration	Activity	Task
	9:00:00 AM	12:30:00 PM	3:30:00		Morning task	JIRA-123
	13:00:00 PM	17:00:00 PM	4:00:00		Afternoon task	JIRA-456
```

Download the sheet as a CSV file to `jira-logs.csv`, then run `jira-log.py -m <month number>`

To use a different CSV filename, use `--input`.

To perform a dry run, use `--dry-run`.
