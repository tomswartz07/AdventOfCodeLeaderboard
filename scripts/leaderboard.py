#!/usr/bin/python

import requests

'''
This script will grab the leaderboard from Advent of Code and post it to Slack
'''

LEADERBOARD = 'http://adventofcode.com/2016/leaderboard/private/view/108855.json'
COOKIES = {'session': 'SESSION_COOKIE'}
# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
SLACK_WEBHOOK = 'https://hooks.slack.com/services/HOOK'

def parseData():
    r = requests.get(LEADERBOARD, cookies=COOKIES)
    if r.status_code == requests.codes.ok:
        RESULTS = r.json()
        str_json = json.dumps(RESULTS)
        data = json.loads(str_json)
        members = data.get('members', None)
        global outputString
        outputString = "Advent of Code Leaderboard as of today:\n"
        outputString += "<http://adventofcode.com/2016/leaderboard/private/view/108855|View Online Leaderboard>\n"
        for value in members.values():
            username = value['name']
            stars = value['stars']
            outputString += username + " : " + str(stars) + " stars\n"
        return outputString

def generatePayload(outputString):
    text = "{\"text\": \"" + outputString + " \"}"
    global PAYLOAD
    PAYLOAD = text
    print(PAYLOAD)
    return PAYLOAD


def postData(PAYLOAD):
    print(PAYLOAD)
    requests.post(
            SLACK_WEBHOOK, data=PAYLOAD,
            headers={'Content-Type': 'application/json'}
            )

parseData()
generatePayload(outputString)
postData(PAYLOAD)
