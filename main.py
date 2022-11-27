# #####
# René Ojeda
# Slang Challenge: Engineering Inter
# #####

import requests

# First Step
# - Fetch API data
activities_response = requests.get("https://api.slangapp.com/challenges/v1/activities",
                                   headers={"Authorization": "key goes here"})


# Second Step
# - Parse received JSON
#   - Separate into user
#   - Separate activities into own sessions
# - Build new data structure


# Third Step
# - Post result to endpoint