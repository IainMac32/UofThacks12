import os
from openai import OpenAI
import re
from dotenv import load_dotenv

load_dotenv()
# Access the API key
ai_key = os.getenv('AIKEY')

client = OpenAI(
    api_key=ai_key
)


UserTopic = "George Washington"

prompt = "What are 3 people or events that are associated with " + UserTopic + " describe " + UserTopic + " from the perspective (first person) of those people or events. Can you put stars around the person / event name (example: **PersonName**) and ## around the descriptions and no other special characters anywhere"

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




print("") #remove later


names_unfiltered = re.findall(r"\*\*(.*?)\*\*", chat_response)

#incase of repeats just don't add them to list
names = []
for name in names_unfiltered:
    if name not in names:
        names.append(name)
print("")
print(names)


print("") #remove later


descs_unfiltered = re.findall(r"\#\#(.*?)\#\#", chat_response)

#incase of repeats just don't add them to list
descs = []
for desc in descs_unfiltered:
    if desc not in descs:
        descs.append(desc)
print("")
print(descs)


