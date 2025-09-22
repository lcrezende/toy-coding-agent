import os
from google.genai import types

def write_file(working_directory, file_path, content):
  full_path = os.path.join(working_directory, file_path)

  allowed = os.path.abspath(working_directory)
  target = os.path.abspath(full_path)

  if not target.startswith(allowed):
    return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'

  if not os.path.exists(full_path):
      os.makedirs(os.path.dirname(full_path), exist_ok=True)

  try:
    with open(full_path, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error: Could not create "{full_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, constrained to the working directory. Creates the file if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=[
            "file_path",
            "content",
        ],
    ),
)