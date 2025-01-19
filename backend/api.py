from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os

from generation import * 
from slides import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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


@app.route("/api/exportSlides", methods=["POST"])
def export_route():
    print("THIS IS CALLED")
    # 1. Get all titles, images, and the chat log for each
    data = request.json


    # 3. Send the title, images, and descriptions to slides.property
    link = create_slideshow(data)

    # 4. return the link ig
    return jsonify({"slides_link": link})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8030))  # Default to 8080
    app.run(debug=True, host='0.0.0.0', port=port)