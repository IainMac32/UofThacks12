from google.oauth2 import service_account
from googleapiclient.discovery import build
import uuid

# Path to your service account key file
SERVICE_ACCOUNT_FILE = "./credentials.json"

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/drive"]
)

# Build the Slides API service
slides_service = build("slides", "v1", credentials=credentials)
drive_service = build("drive", "v3", credentials=credentials)

def initializePresentation(title):
    # Create a new blank presentation
    presentation = slides_service.presentations().create(body={"title": title}).execute()

    # Get the presentation ID and URL
    presentation_id = presentation.get("presentationId")
    print(f"Created presentation with ID: {presentation_id}")
    print(f"View it at: https://docs.google.com/presentation/d/{presentation_id}/edit")

    # Make the presentation public to any viewer
    drive_service.permissions().create(
        fileId=presentation_id,
        body={
            "role": "reader",  # "reader" for view-only, or "writer" for edit access
            "type": "anyone",  # Makes it accessible to anyone with the link
        }
    ).execute()

    return presentation_id

def addContentToSlide(presentation_id, title, image_url, description):
    # Create a new blank slide
    requests = [
        {
            "createSlide": {
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }
        }
    ]
    response = slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()
    
    # Get the slide ID of the newly created slide
    slide_id = response['replies'][0]['createSlide']['objectId']

    # Define element IDs for title, image, and description
    title_id = f"title_{str(uuid.uuid4())}"
    image_id = f"image_{str(uuid.uuid4())}"
    description_id = f"description_{str(uuid.uuid4())}"

    # Add the title, image, and description to the slide
    requests = [
        # Add title text box
        {
            "createShape": {
                "objectId": title_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 50, "unit": "PT"},
                        "width": {"magnitude": 500, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,  # Horizontal scale (1 = normal)
                        "scaleY": 1,  # Vertical scale (1 = normal)
                        "translateX": 50,  # X position (in points)
                        "translateY": 50,  # Y position (in points)
                        "unit": "PT"
                    },
                },
            }
        },
        {
            "insertText": {
                "objectId": title_id,
                "insertionIndex": 0,
                "text": title,
            }
        },
        # Add image
        {
            "createImage": {
                "objectId": image_id,
                "url": image_url,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 200, "unit": "PT"},
                        "width": {"magnitude": 300, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 50,
                        "translateY": 150,
                        "unit": "PT"
                    },
                },
            }
        },
        # Add description text box
        {
            "createShape": {
                "objectId": description_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 100, "unit": "PT"},
                        "width": {"magnitude": 500, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 50,
                        "translateY": 400,
                        "unit": "PT"
                    },
                },
            }
        },
        {
            "insertText": {
                "objectId": description_id,
                "insertionIndex": 0,
                "text": description,
            }
        },
    ]

    # Execute the batch update request
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()

def handleData(data):

    # Extract data from the dictionary
    title = data.get("title")  # Default title if not provided
    image = data.get("image")  # Default to empty string if no image is provided
    description = data.get("description")  # Default to empty string if no description is provided

    # Call the addContentToSlide function to add a slide with the extracted data
    addContentToSlide(
        presentation_id=presentation_id, 
        title=title, 
        image_url=image, 
        description=description
    )


presentation_id = initializePresentation("UofTHacks")
json = {
    "title": "Placeholder title",
    "image": "https://pokemonletsgo.pokemon.com/assets/img/common/char-pikachu.png",
    "description": ";laskdj;lkasdjf;lkasdjfl;askdjf"
}
handleData(json)