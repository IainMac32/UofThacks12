from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from generation import * 

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# GLOBAL VARIABLES


# ROUTES 

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route("/api/getPerspectives", methods=['POST', 'GET', 'OPTIONS'])
def submit_perspectives():

    topic = request.json.get('topic')
    print(topic)

    # perspectives_dict contains {"names": [names], "images": [image urls], "descs": [descriptions]}
    perspectives_dict = get_perspectives(topic)
    
    return jsonify(perspectives_dict)

@app.route("/api/chatbot", methods=["POST"])
def chatbot_route():
    data = request.json
    user_question = data.get("user_question")
    user_topic = data.get("user_topic")
    past_response = data.get("past_response")

    # Validate input
    if not user_question or not user_topic or past_response is None:
        return jsonify({"error": "Missing required parameters"}), 400

    # Call the get_chatbot method
    response = get_chatbot(user_question, user_topic, past_response)
    print(response)

    # Return the chatbot response
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

