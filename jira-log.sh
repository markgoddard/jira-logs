#!/bin/bash

# Adapted from https://gist.github.com/patrick-blom/593dd02338490941f4ba09f714e821c3

# Example:
# ./jira-log.sh -i SHPC-2377 -t 165 -c "Ansible error handling" -s '2021-11-09T11:00:00.000+0000'

set -e

####add a worklog to a specific jira issue####

#arguments:
#-i: issue or ticket number
#-t: time in minutes
#-c: comment for the worklog

#optional:
#-u: jira user, if not defined in script

####example
#worklog -i SCRUM-42 -t 15 -c "Daily Scrum" 

#####configuration
jiraDomain="https://stackhpc.atlassian.net"
#####configuration

for arg in "$@"
do
    if [ "$arg" == "--help" ] || [ "$arg" == "-h" ]
    then
        echo -e "####add a worklog to a specific jira issue####"
        echo -e ""
        echo -e "arguments:"
        echo -e "-i: issue or ticket number"
        echo -e "-t: time in minutes"
        echo -e "-c: comment for the worklog"
        echo -e "-s: start datetime"
        echo -e ""
        echo -e "optional:"
        echo -e "-u: jira user, if not defined in script"
        echo -e ""
        echo -e "####example"
        echo -e "$0 -i SHPC-2377 -t 165 -c \"Ansible error handling\" -s \"2021-11-09T11:00:00.000+0000\""
        exit 0
    fi
done

while getopts u:i:t:c:s: option
do
case "${option}"
in
u) jiraUser=${OPTARG};;
i) issue=${OPTARG};;
t) timeInSeconds=$((${OPTARG}* 60));;
c) comment="${OPTARG}";;
s) currentDateTime="${OPTARG}";;
esac
done

if [[ -z $currentDateTime ]]; then
        currentDateTime=$(date -u +"%Y-%m-%dT%H:%M:%S.000+0000")
fi

if [[ -z "$issue" || -z "$timeInSeconds" || -z "$comment" ]]; then
        echo -e "the paramters -i, -t and -c are requiered!"
        echo -e "use --help or -h for help"
        exit 1
fi

if [[ -f ~/.jira-user ]]; then
        jiraUser=$(cat ~/.jira-user)
else
    if [ -z "$jiraUser" ]; then
        read -p "Enter Username: " jiraUser
    fi
fi

if [[ -f ~/.jira-api-token ]]; then
        jiraPswd=$(cat ~/.jira-api-token)
else
        read -s -p "Enter Password: "  jiraPswd
fi

echo -e "";

dataString=$( jq -n \
                  --arg c "$comment" \
                  --arg cdt "$currentDateTime" \
                  --arg t "$timeInSeconds" \
                  '{comment:$c,started:$cdt,timeSpentSeconds:$t}')

curl --fail -u $jiraUser:$jiraPswd -H "Content-Type: application/json" -X POST "$jiraDomain/rest/api/2/issue/$issue/worklog" -d "$dataString"
