import requests
from requests.auth import HTTPBasicAuth
from config import JIRA_USERNAME, JIRA_TOKEN, JIRA_URL
from bedrock import bedrock_chain, run_chain


# Jira authentication details
username = JIRA_USERNAME
api_token = JIRA_TOKEN  # You can generate this from Jira settings


# Get Payload from Bedrock

state = {}
state["llm_chain"] = bedrock_chain()
state["questions"], state["answers"] = [], []

llm_chain = state['llm_chain']

input = "Not able to add element to array."
result, amount_of_tokens = run_chain(llm_chain, input)
question_with_id = {
    "question": input,
    "id": len(state['questions']),
    "tokens": amount_of_tokens,
}
state['questions'].append(question_with_id)

state['answers'].append(
    {"answer": result, "id": len(state['questions'])}
)



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