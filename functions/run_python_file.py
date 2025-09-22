import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
  full_path = os.path.join(working_directory, file_path)
  
  allowed = os.path.abspath(working_directory)
  target = os.path.abspath(full_path)
  
  if not target.startswith(allowed):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(full_path):
    return f'Error: File "{file_path}" not found.'

  if not full_path.endswith('.py'):
    return f'Error: "{file_path}" is not a Python file.'

  try:
    result = subprocess.run(
      ['python', file_path, *args], 
      cwd=working_directory,
      timeout=30,
      capture_output=True
    )
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    output = f"STDOUT: {stdout}\nSTDERR: {stderr}"
    if result.returncode != 0:
      output += f"\nProcess exited with code {result.returncode}"
    if not stdout.strip() and not stderr.strip():
      return "No output produced."
    return output
  except Exception as e:
    return f"Error: executing Python file: {e}"