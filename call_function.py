from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    working_directory = "./calculator"
    
    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(working_directory, **function_call_part.args)
        case "get_file_content":
            function_result = get_file_content(working_directory, **function_call_part.args)
        case "run_python_file":
            function_result = run_python_file(working_directory, **function_call_part.args)
        case "write_file":
            function_result = write_file(working_directory, **function_call_part.args)
        case _:
            return types.Content(
                role = "function",
                parts = [
                    types.Part.from_function_response(
                        name = function_call_part.name,
                        response = {"error": f"Unknown function: {function_call_part.name}"}
                    )
                ]
            )
    
    return types.Content(
        role = "function",
        parts = [
            types.Part.from_function_response(
                name = function_call_part.name,
                response = {"result": function_result}
            )
        ]
    )

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

