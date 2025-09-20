import os

def get_file_content(working_directory, file_path):
  full_path = os.path.join(working_directory, file_path)

  allowed = os.path.abspath(working_directory)
  target = os.path.abspath(full_path)

  if not target.startswith(allowed):
    return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(full_path):
    return f'Error: "{full_path}" is not a file'
  
  MAX_CHARS = 10000

  try:
    with open(full_path, "r") as f:
      file_content_string = f.read(MAX_CHARS) + "[...File truncated at 10000 characters]"
  except Exception as e:
    return f'Error: Cannot read "{full_path}": {e}'
  
  return file_content_string  