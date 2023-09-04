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

A template work log in Google Sheets is available [here](https://docs.google.com/spreadsheets/d/1SiIWsMwz4xZgtgDISr6TVy1xZ66eLzjQeRDgsE4W0A8/edit).

Download the sheet as a CSV file to `jira-logs.csv`, then run `jira-log.py -m <month number>`

To use a different CSV filename, use `--input`.

To perform a dry run, use `--dry-run`.

### Deleting logs
Sometimes you make a mistake. It's OK, we've all been there.

If you've done something wrong whilst uploading your logs (e.g. wrong month, wrong ticket, wrong career), the output of your previous job is stored in `output.log` - so don't delete this. You can run `jira-delete.sh` to remove any worklogs in this file from jira. 
