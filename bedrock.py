import os
import boto3
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from jira import fetch_issues

print("Imported all modules")

os.environ['AWS_PROFILE'] = 'bedrock-admin'

def bedrock_chain():
    profile = 'bedrock-admin'

    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2",
    )

    claude = Bedrock(
        model_id="anthropic.claude-v2", client=bedrock_runtime, credentials_profile_name=profile
    )
    claude.model_kwargs = {
        "temperature": 0.1, 
        "max_tokens_to_sample": 2048,
        "top_k": 250,
        "top_p": 1,
    }
    
    
    prompt_template = """You are a bot used for tech support. You will be asked questions based on the provided information.

    The user will ask a question, based on the question, look through the codebase to see if you find similar code, and share a potential reason why the user is facing the issue; and if there is an existing ticket for it, based on the ones you remember.
    If you're not able to find code that is related to the specified issue, or if you're not able to find a similar existing support ticket, explicitly mention that. 
    
    The existing tickets and codebase will be provided as context in the first input.
    
    Existing Tickets will be provided with their ticket IDs followed by their title.
    The codebase will contain the name of the file and the code inside of it. 
    
    Current conversation:
    {history}
    
    User: {input}
    Bot:"""
    
    
    # make sure you feed the PromptTemplate with the new variables
    PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=prompt_template
    )

    memory = ConversationBufferMemory(human_prefix="User", ai_prefix="Bot")
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=claude,
        verbose=True,
        memory=memory,
    )

    return conversation
    
def run_chain(chain, prompt):
    num_tokens = chain.llm.get_num_tokens(prompt)
    
    return chain({"input": prompt}), num_tokens


def clear_memory(chain):
    return chain.memory.clear()

def generate_prompt_template():
    
    from github_file_content import list_files_and_content_in_repo
    
    username = "sreekeshiyer"
    repo_name = "python-sample-codebase"
    
    prompt = list_files_and_content_in_repo(username, repo_name)
    
    return prompt
    
 
def initialize():
    
    code = generate_prompt_template()
    
    all_tickets = '\n'.join([f"{i['key']: i['summary']}" for i in fetch_issues()])
    
    issues = f"""
    Existing Tickets:
    {all_tickets}
    """
    
    codebase = f"""\nCodebase: 
    {code}
    """   
    
    context= issues+codebase
    llm_chain = bedrock_chain()
    result, amount_of_tokens = run_chain(llm_chain, context)
    
    return llm_chain


def analyse_ticket(chain, input_from_user):
    
    result, amount_of_tokens = run_chain(chain, input_from_user)
    return result['response']