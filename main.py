# #####
# René Ojeda
# Slang Challenge: Engineering Inter
# #####

# env Variables
from env import AUTH_TOKEN
import requests

# First Step
# - Fetch API data
activities_response = requests.get("https://api.slangapp.com/challenges/v1/activities",
                                   headers={"Authorization": AUTH_TOKEN})


# Second Step
# - Parse received JSON
#   - Separate into user
#   - Separate activities into own sessions
# - Build new data structure

def build_user_sessions():
    pass

user_sessions = {"user_sessions": build_user_sessions(activities_response.json())}


# Third Step
# - Post result to endpoint

requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
              headers={"Authorization": AUTH_TOKEN},
              json=user_sessions)
