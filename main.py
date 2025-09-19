import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


verbose = False
if "--verbose" in sys.argv:
    verbose = True
if len(sys.argv) < 2:
    print("No prompt provided")
    sys.exit(1)
user_prompt = sys.argv[1]


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages
)
print("\n" + response.text)

if verbose:
    print("\n")
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
