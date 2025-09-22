import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose, 0)


def generate_content(client, messages, verbose, iteration=0):
    if iteration == 20:
        raise Exception("max iterations reached")
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        )
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

    if not response.function_calls:
        print (response.text)
        return
    
    for candidate in response.candidates:
        messages.append(candidate.content)

    for function_call in response.function_calls:
        try:
            function_result = call_function(function_call, verbose)
            if verbose:
                print(f"-> {function_result.parts[0].function_response.response}")
            messages.append(function_result)
        except Exception as e:
            print(f"Error calling function: {e}")
            messages.append(types.Content(role="function", parts=[types.Part.from_function_response(name=function_call.name, response={"error": str(e)})]))
        
    
    generate_content(client, messages, verbose, iteration + 1)


if __name__ == "__main__":
    main()