import os

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