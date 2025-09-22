import os
from google.genai import types

def get_files_info(working_directory, directory="."):
  full_path = os.path.join(working_directory, directory)

  allowed = os.path.abspath(working_directory)
  target = os.path.abspath(full_path)

  if not target.startswith(allowed):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(full_path):
    return f'Error: "{directory}" is not a directory'
  
  contents = os.listdir(full_path)
  contents_info = []

  for item in contents:
    item_path = os.path.join(full_path,item)
    try:
      contents_info.append(f"- {item}: size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
    except Exception as e:
      contents_info.append(f"- {item}: error getting info: {e}")

  return "\n".join(contents_info)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)