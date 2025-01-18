from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = "./credentials.json"

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/presentations"]
)

# Build the Slides API service
service = build("slides", "v1", credentials=credentials)

# Create a new blank presentation
presentation = service.presentations().create(body={"title": "My Blank Presentation"}).execute()

# Get the presentation ID and URL
presentation_id = presentation.get("presentationId")
print(f"Created presentation with ID: {presentation_id}")
print(f"View it at: https://docs.google.com/presentation/d/{presentation_id}/edit")
