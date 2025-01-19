import os
from openai import OpenAI
import re
from dotenv import load_dotenv
import requests


# flask for different pov creation of 4 people and images (creates a dictionary)
def get_perspectives(topic):
    # load api key
    load_dotenv()
    ai_key = os.getenv('AIKEY')
    client = OpenAI(api_key=ai_key)
    google_key = os.getenv('GKEY')

    # --------------------------------------------------
    UserTopic = topic

    prompt = "What are 3 people or events that are associated with " + UserTopic + " describe " + UserTopic + " from the perspective (first person) of those people or events. First have " + UserTopic + " describe themselves from their own perspective. Can you put stars around the person / event name (example: **PersonName**) and ## around the descriptions (##description##) and no other special characters anywhere"


    # GPT response --------------------------------------------------
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )


    # Get the response from the API
    response_text = chat_completion.choices[0].message.content

    # Save the response to a file
    if response_text:
        chat_response = response_text
        print("ChatGPT Response:")
        print(chat_response)
    else:
        print("Failed to get a response.")



    #get names list -------------------------
    names_unfiltered = re.findall(r"\*\*(.*?)\*\*", chat_response)

    #incase of repeats just don't add them to list
    names = []
    for name in names_unfiltered:
        if name not in names:
            names.append(name)



    #get descriptions list -------------------------
    descs_unfiltered = re.findall(r"\#\#(.*?)\#\#", chat_response)

    #incase of repeats just don't add them to list
    descs = []
    for desc in descs_unfiltered:
        if desc not in descs:
            descs.append(desc)


    # google images search --------------------------------------------------
    API_KEY = google_key
    SEARCH_ENGINE_ID = '202048886b2a0438d'

    def fetch_image_urls(query, num_results):
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "cx": SEARCH_ENGINE_ID,
            "key": API_KEY,
            "searchType": "image",
            "num": num_results,
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            image_urls = [item["link"] for item in results.get("items", [])]
            return image_urls
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []

    # image url list --------------------------------------------------
    images_url = []
    for name in names:
        images_url.append(fetch_image_urls(name,1)[0])


    # setup return dictionary -------------------------
    dict = {}
    dict["names"] = names
    dict["descs"] = descs
    dict["images"] = images_url
    
    return dict





# in flask for talking to person
def get_chatbot(user_question,user_topic,past_response):
    load_dotenv()
    ai_key = os.getenv('AIKEY')
    client = OpenAI(api_key=ai_key)

    # GPT response --------------------------------------------------
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are {user_topic}. SPEAK IN FIRST PERSON from the knowledge and perspective of you!"},
            {"role": "assistant", "content": past_response},
            {"role": "user", "content": user_question},
        ],
        model="gpt-4o",
    )


    # Get the response from the API
    response_text = chat_completion.choices[0].message.content
    return response_text

