import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
  full_path = os.path.join(working_directory, file_path)

  allowed = os.path.abspath(working_directory)
  target = os.path.abspath(full_path)

  if not target.startswith(allowed):
    return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(full_path):
    return f'Error: "{full_path}" is not a file'
  
  try:
    with open(full_path, "r") as f:
      file_content_string = f.read(MAX_CHARS) + f"[...File truncated at {MAX_CHARS} characters]"
  except Exception as e:
    return f'Error: Cannot read "{full_path}": {e}'
  
  return file_content_string  

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and return the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the content of, relative to the working directory.",
            ),
        },
    ),
)