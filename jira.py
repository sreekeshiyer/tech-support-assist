import requests
from requests.auth import HTTPBasicAuth
from config import JIRA_USERNAME, JIRA_TOKEN, JIRA_URL

# Jira authentication details
username = JIRA_USERNAME
api_token = JIRA_TOKEN  # You can generate this from Jira settings


# Comment payload
import json

def comment_on_ticket(key, text):
  
  # Base URL for your Jira instance
  base_url = JIRA_URL
  
  # Endpoint to comment on an issue
  url = f"{base_url}/rest/api/3/issue/{key}/comment"
  
  # Set up authentication
  auth = HTTPBasicAuth(username, api_token)
  
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }

  
  comment_text = text
  payload = json.dumps( {
    "body": {
      "content": [
        {
          "content": [
            {
              "text": text,
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    # "visibility": {
    #   "identifier": "Administrators",
    #   "type": "role",
    #   "value": "Administrators"
    # }
  } )
  
  # Make the API request
  response = requests.request(
     "POST",
     url,
     data=payload,
     headers=headers,
     auth=auth
  )
  
  #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  
  # Check the response
  if response.status_code == 201:
      print("Comment added successfully!")
  else:
      print(f"Failed to add comment. Status code: {response.status_code}, Message: {response.text}")
      
      
def fetch_issues():
  
  url = f"{JIRA_URL}/rest/api/3/search"
  
  # Set up authentication
  auth = HTTPBasicAuth(username, api_token)
  
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }
  
  query = {
  'jql': 'project = ZA'
  }

  response = requests.request(
     "GET",
     url,
     headers=headers,
     params=query,
     auth=auth
  )
  
  if response.status_code == 200:
    # Parse the JSON response
    issues = response.json()
    
    res = []
    
    # Process and print the issues
    for issue in issues['issues']:
        res.append(
            {
              "key": issue['key'],
              "summary": issue['fields']['summary']
            }
          )
    return res
  else:
      # Print an error message if the request was not successful
      return []