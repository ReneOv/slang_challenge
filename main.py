# #####
# René Ojeda
# Slang Challenge: Engineering Inter
# #####

# env Variables
from env import AUTH_TOKEN
import requests
import json
from datetime import datetime as dt

# Helper functions

def differenceInSeconds(date1, date2) -> float:
    parsedDate1 = dt.strptime(date1, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    parsedDate2 = dt.strptime(date2, '%Y-%m-%dT%H:%M:%S.%f+00:00')

    return (parsedDate1 - parsedDate2).total_seconds()

def appendIdArray(array: list, newId) -> list:
    return array + [newId]


# First Step
# - Fetch API data
activities_response = requests.get("https://api.slangapp.com/challenges/v1/activities",
                                   headers={"Authorization": AUTH_TOKEN})

print("GET Response: ", activities_response)


# Second Step
# - Parse received JSON
#   - Separate into user
#   - Separate activities into own sessions
# - Build new data structure

def build_user_sessions(activities_response) -> any:        # O(N)
    user_sessions = {}
    for activity in activities_response['activities']:      # O(N) - It only iterates through the activity response json once. It mutates the dictionary and updates values every time a new entry is read.
        if activity["user_id"] in user_sessions.keys():     # O(1) - Dictionaries in Python don't iterate to find keys, since they are hashed.
            current = len(user_sessions[activity["user_id"]]) - 1
            if differenceInSeconds(activity["first_seen_at"], user_sessions[activity["user_id"]][current]["ended_at"]) > 300.0:   # It means that the new activity belongs to a different session.
                user_sessions[activity["user_id"]] = appendIdArray(user_sessions[activity["user_id"]] ,{
                    "started_at": activity["first_seen_at"],
                    "ended_at": activity["answered_at"],
                    "activity_ids": [
                        activity["id"]
                    ],
                    "duration_seconds": differenceInSeconds(activity["answered_at"], activity["first_seen_at"])
                })
            else:                   # Belongs to the most recent session.                                                                                   
                user_sessions[activity["user_id"]][current] = {
                    "started_at": user_sessions[activity["user_id"]][current]["started_at"],
                    "ended_at": activity["answered_at"],                # Update new end date
                    "activity_ids": appendIdArray(user_sessions[activity["user_id"]][current]["activity_ids"], (activity["id"])),
                    "duration_seconds": differenceInSeconds(activity["answered_at"], user_sessions[activity["user_id"]][current]["started_at"])       # Update session duration
                }

        else:
            user_sessions[activity["user_id"]] = [{
                "started_at": activity["first_seen_at"],
                "ended_at": activity["answered_at"],
                "activity_ids": [
                    activity["id"]
                ],
                "duration_seconds": differenceInSeconds(activity["answered_at"], activity["first_seen_at"])
            }]
    
    return user_sessions
    
    

user_sessions = {"user_sessions": build_user_sessions(activities_response.json())}


# Third Step
# - Post result to endpoint

solution_response = requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
            headers={"Authorization": AUTH_TOKEN},
            json=user_sessions)

print("POST Response: ", solution_response)