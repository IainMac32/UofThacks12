from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os

from generation import * 
from slides import *
from databricksDB import *

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


import time

@app.route("/api/exportSlides", methods=["POST"])
def export_route():
    print("THIS IS CALLED")
    # 1. Get all titles, images, and the chat log for each
    data = request.json

    max_retries = 4
    attempt = 0
    link = None

    # Retry loop to create slideshow link
    while attempt < max_retries:
        try:
            # 3. Send the title, images, and descriptions to slides.property
            link = create_slideshow(data)
            break  # Break the loop if successful
        except Exception as e:
            attempt += 1
            print(f"Error creating slideshow: {e}. Retrying {attempt}/{max_retries}...")
            time.sleep(2)  # Wait 2 seconds before retrying

    if link is None:
        return jsonify({"error": "Failed to create slideshow after multiple attempts"}), 500

    # 4. Upload the link to the database
    names = data.get("names")[0]
    upload_to_db(names, link)

    # Return the link
    return jsonify({"slides_link": link})


@app.route("/api/retrieve_db", methods=["POST"])
def export_db_route():
    print("THIS IS CALLED")
    # 1. Get all titles, images, and the chat log for each
    

    # 4. return the link ig
    return jsonify(retrieve_from_db())





if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8030))  # Default to 8080
    app.run(debug=True, host='0.0.0.0', port=port)

