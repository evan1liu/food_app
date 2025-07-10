import google.genai as genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
# Configure the client with API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Give me 10 super markets with a web database and website that are the closest to 35 N Park Street, Madison, wisconsin. Arrange the super markets from nearest to farthest",
    config=config,
)

# Print the grounded response
print(response.text)