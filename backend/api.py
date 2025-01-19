from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os

from generation import * 
from slides import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
    # 1. Get all titles, images, and the chat log for each
    data = request.json
    titles = data.get("titles")
    chat_logs = data.get("chat_logs")
    topic = data.get("topic")
    # note there is also data.get("images") but we don't need to use it just yet

    # 2. Convert the chat log to a slide description
    descriptions = [] # convert each chat log to a description
    for i in range(len(titles)):
        descriptions.append(convert_chat_logs(chat_logs[i], titles[i]))

    data["descs"] = descriptions

    # 3. Send the title, images, and descriptions to slides.property
    link = create_slideshow(data, topic)

    # 4. return the link ig
    return jsonify({"slides_link": link})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Default to 8080
    app.run(debug=True, host='0.0.0.0', port=port)