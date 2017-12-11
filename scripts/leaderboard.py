#!/usr/bin/env python

'''
This script will grab the leaderboard from Advent of Code and post it to Slack
'''

import datetime, json, requests

# see README for directions on how to fill these variables
LEADERBOARD_ID = ""
SESSION_ID = ""
SLACK_WEBHOOK = ""

def formatLeaderMessage(members):
    message = ""

    # add each member to message
    for username, score, stars in members:
        message += "\n*{}* {} Points, {} Stars".format(username, score, stars)

    message += "\n\n<{}|View Online Leaderboard>".format(LEADERBOARD_URL)

    return message

def parseMembers(members_json):
    # get member name, score and stars
    members = [(m["name"], m["local_score"], m["stars"]) for m in members_json.values()]

    # sort members by score, decending
    members.sort(key=lambda s: (-s[1], -s[2]))

    return members

def postMessage(message):
    payload = json.dumps({
        "icon_emoji": ":christmas_tree:",
        "username": "Advent Of Code Leaderboard",
        "text": message
    })

    requests.post(
        SLACK_WEBHOOK,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

def main():
    # make sure all variables are filled
    if LEADERBOARD_ID == "" or SESSION_ID == "" or SLACK_WEBHOOK == "":
        print("Please update script variables before running script.\nSee README for details on how to do this.")
        exit(1)

    global LEADERBOARD_URL
    LEADERBOARD_URL = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(datetime.datetime.today().year, LEADERBOARD_ID)

    # retrieve leaderboard
    r = requests.get(
        "{}.json".format(LEADERBOARD_URL),
        cookies={"session": SESSION_ID}
    )
    if r.status_code != requests.codes.ok:
        print("Error retrieving leaderboard")
        exit(1)

    # get members from json
    members = parseMembers(r.json()["members"])

    # generate message to send to slack
    message = formatLeaderMessage(members)

    # send message to slack
    postMessage(message)

if __name__ == "__main__":
    main()
