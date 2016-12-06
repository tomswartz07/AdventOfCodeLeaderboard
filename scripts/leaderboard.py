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
        members = r.json()["members"]
        global outputString
        outputString = "Advent of Code Leaderboard as of today:\n"
        outputString += "<http://adventofcode.com/2016/leaderboard/private/view/108855|View Online Leaderboard>\n"

        # get all members
        users = [(m["name"], m["stars"]) for m in members.values()]
        # sort members by stars decending
        users.sort(key=lambda s: -s[1])
        # add each user to outputString
        for username, stars in users:
            outputString += "{}: {} stars\n".format(username, stars)

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
