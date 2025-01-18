from google.oauth2 import service_account
from googleapiclient.discovery import build
import uuid
import webbrowser

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

    element_id = f"MyTextBox_{str(uuid.uuid4())}"  # Use uuid to generate a unique ID


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
                        "height": {"magnitude": 60, "unit": "PT"},
                        "width": {"magnitude": 480, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,  # Horizontal scale (1 = normal)
                        "scaleY": 1,  # Vertical scale (1 = normal)
                        "translateX": 10,  # X position (in points)
                        "translateY": 10,  # Y position (in points)
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
            },
        },
        {
            "updateTextStyle": {
                "objectId": title_id,
                "style": {
                    "bold": True,
                    "fontSize": {"magnitude": 30, "unit": "PT"},
                    "foregroundColor": {
                        "opaqueColor": {"rgbColor": {"red": 0, "green": 0, "blue": 0}}
                    },
                },
                "fields": "bold,fontSize,foregroundColor",
                "textRange": {
                    "type": "ALL"  # This applies the style to all text in the object
                }
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
                        "height": {"magnitude": 250, "unit": "PT"},
                        "width": {"magnitude": 350, "unit": "PT"}
                    }, #350,450,125,50
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 420,
                        "translateY": 20,
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
                        "height": {"magnitude": 400, "unit": "PT"},
                        "width": {"magnitude": 480, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 10,
                        "translateY": 75,
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

        {
            "updateTextStyle": {
                "objectId": description_id,
                "style": {
                    "fontSize": {"magnitude": 18, "unit": "PT"},
                    "foregroundColor": {
                        "opaqueColor": {"rgbColor": {"red": 0, "green": 0, "blue": 0}}
                    },
                },
                "fields": "bold,fontSize,foregroundColor",
                "textRange": {
                    "type": "ALL"  # This applies the style to all text in the object
                }
            }
        }
    ]

    # Execute the batch update request
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()

    background_color_request = {
        "updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {
                        "color": {
                            "rgbColor": {"red": 0.94, "green": 0.87, "blue": 0.73}  # Light gray color
                        }
                    }
                }
            },
            "fields": "pageBackgroundFill"
        }
    }

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": [background_color_request]}
    ).execute()







def handleData(data,presentation_id):

    # Extract data from the dictionary
    title = data.get("names")  # Default title if not provided
    image = data.get("images")  # Default to empty string if no image is provided
    description = data.get("descs")  # Default to empty string if no description is provided

    for i in range(len(title)):
        # Call the addContentToSlide function to add a slide with the extracted data
        addContentToSlide(
            presentation_id=presentation_id,
            title=title[i], 
            image_url=image[i], 
            description=description[i]
        )


def create_slideshow(json,topic):
    presentation_id = initializePresentation("UofTHacks")

    # delete first slide
    credentials_file = 'credentials.json'
    creds = service_account.Credentials.from_service_account_file(credentials_file)
    service = build("slides", "v1", credentials=creds)
    requests = [{"deleteObject": {"objectId": "p",}}]
    body = {"requests": requests}
    response = (service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute())


    json = {
        "names": ["Placeholder title","test"],
        "images": ["https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg/1200px-Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg","https://www.varsitytutors.com/images/earlyamerica/washington.jpg"],
        "descs": [";laskdj;lkasdjf;lkasdjfl;askdjf","Slides about George. Slides about George. Slides about George. Slides about George. Slides about George. Slides about George. "]
    }
    handleData(json,presentation_id)

    presentation_link = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    return presentation_link
