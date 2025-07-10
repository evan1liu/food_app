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
    contents="Give me the price for a dozen of eggs in the Fresh Madison Market at 703 University Ave, Madison.",
    config=config,
)

# Print the grounded response
print(response.text)