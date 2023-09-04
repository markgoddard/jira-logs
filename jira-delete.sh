#!/bin/bash 
set -eu 

#####configuration
jiraUser="tyler@stackhpc.com"
jiraDomain="https://stackhpc.atlassian.net"
#####configuration

if [[ -f ~/.jira-api-token ]]; then
        jiraPswd=$(cat ~/.jira-api-token)
else
        read -s -p "Enter Password: "  jiraPswd
fi

grep -o '/issue/[0-9]\+/worklog/[0-9]\+' output.log | awk -F'/' '{issue_id=$3; worklog_id=$5; print issue_id, worklog_id}' | while read -r issue_id worklog_id
do
    echo "Issue ID: $issue_id"
    echo "Worklog ID: $worklog_id"
    curl --fail -u $jiraUser:$jiraPswd -H "Content-Type: application/json" -X DELETE "$jiraDomain/rest/api/2/issue/$issue_id/worklog/$worklog_id"
    echo "Deleted."
done

