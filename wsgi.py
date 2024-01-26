from flask import Flask, jsonify, request
import bedrock
from jira import comment_on_ticket

app = Flask(__name__)
chain = bedrock.initialize()
replied = []

@app.route('/comment', methods=["POST"])
def comment():
    
    data = request.get_json()
    
    key=data["key"]
    title = data["title"]
    description = data["description"]
    
    if key not in replied:
        print("Commenting on Issue:", key)
        
        input_from_user = f"""There is a new ticket.
            Title: {title}
            Description: {description}
            
            Please help out.  
        """
        res = bedrock.analyse_ticket(chain, input_from_user)
        
        comment_text = res
        
        comment_on_ticket(key, comment_text)
        
        replied.append(key)
    
    return jsonify({
        "message": "Success"
    })


if __name__ == '__main__':
    
    app.run()