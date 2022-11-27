# #####
# René Ojeda
# Slang Challenge: Engineering Inter
# #####

# env Variables
from env import AUTH_TOKEN
import requests
import sys
import json
from datetime import datetime as dt

# Helper functions
def differenceInSeconds(date1, date2) -> float:
    parsedDate1: dt.strptime(date1, '%Y-%m-%dT%H:%M:%S.%fZ')
    parsedDate2: dt.strptime(date2, '%Y-%m-%dT%H:%M:%S.%fZ')

    return (parsedDate2 - parsedDate1).total_seconds()

# First Step
# - Fetch API data
# activities_response = requests.get("https://api.slangapp.com/challenges/v1/activities",
#                                    headers={"Authorization": AUTH_TOKEN})

# Save to file to not call API every time
# sys.stdout = open('response.json', 'w')
# print(json.dumps(activities_response.json()))

activities_response = json.load(open('response.json'))

print(activities_response['activities'][0])


# Second Step
# - Parse received JSON
#   - Separate into user
#   - Separate activities into own sessions
# - Build new data structure

def build_user_sessions(activities_response):               # O(N)
    user_sessions = {}
    for activity in activities_response['activities']:      # O(N)
        if activity["user_id"] in user_sessions.keys():     # O(1) 
            if differenceInSeconds(activity["first_seen_at"], user_sessions["user_id"]["ended_at"]) > 300:   # It means that the new activity belongs to a different session.
                user_sessions["user_id"].append({
                    "started_at": activity["first_seen_at"],
                    "ended_at": activity["answered_at"],
                    "activity_ids": [
                        activity["id"]
                    ],
                    "duration_seconds": differenceInSeconds(activity["answered_at"], activity["first_seen_at"])
                })
            else:                   # Belongs to the most recent session.
                current = len(user_sessions["user_id"]) - 1                                                                                        
                user_sessions["user_id"][current] = {
                    "ended_at": activity["answered_at"],                # Update new end date
                    "activity_ids": user_sessions["user_id"][current]["activity_ids"].append(activity["id"]),
                    "duration_seconds": differenceInSeconds(activity["answered_at"], user_sessions["user_id"][current]["started_at"])       # Update session duration
                }

        else:
            print(activity)
            user_sessions["user_id"] = [{
                "started_at": activity["first_seen_at"],
                "ended_at": activity["answered_at"],
                "activity_ids": [
                    activity["id"]
                ],
                "duration_seconds": differenceInSeconds(activity["answered_at"], activity["first_seen_at"])
            }]

user_sessions = {"user_sessions": build_user_sessions(activities_response)}

sys.stdout = open('solution.json', 'w')
print(json.dumps(user_sessions))


# Third Step
# - Post result to endpoint

# requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
#             headers={"Authorization": AUTH_TOKEN},
#             json=user_sessions)