#!/usr/bin/env python

'''
This script will grab the leaderboard from Advent of Code and post it to Slack
'''

import requests

# see README for directions on how to fill these variables
LEADERBOARD_ID = ""
SESSION_ID = ""
SLACK_WEBHOOK = ""

def parseData():
    r = requests.get(
        "http://adventofcode.com/2016/leaderboard/private/view/{}.json".format(LEADERBOARD_ID),
        cookies={"session": SESSION_ID}
    )
    if r.status_code == requests.codes.ok:
        members = r.json()["members"]
        global outputString
        outputString = "Advent of Code Leaderboard as of today:\n"
        outputString += "<http://adventofcode.com/2016/leaderboard/private/view/{}|View Online Leaderboard>\n".format(LEADERBOARD_ID)

        # Get all members
        users = [(m["name"], m["local_score"], m["stars"]) for m in members.values()]
        # Sort members by score, decending
        users.sort(key=lambda s: -s[1])
        # Add each user to outputString
        for username, score, stars in users:
            outputString += "{}: {} Points, {} Stars\n".format(username, score, stars)
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
        headers={"Content-Type": "application/json"}
        )

parseData()
generatePayload(outputString)
postData(PAYLOAD)
