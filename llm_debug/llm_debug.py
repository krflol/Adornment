import subprocess

import os
import traceback
import inspect
from functools import wraps
from dotenv import load_dotenv
from langchain.llms import OpenAI
import openai
# Load environment variables
load_dotenv()
# Initialize LangChain's LLM with GPT-4 using the API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4-1106-preview")
openai.api_key = OPENAI_API_KEY
md_response = []
def llm_debugger(reflections=1, output='error_response.md', additional_context=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Exception: '{e}' being sent to LLM for debugging")
                # Get the content of the function (source code)
                function_content = inspect.getsource(func)
                # Get the inputs that caused the error
                inputs = f"Inputs: args={args}, kwargs={kwargs}"
                # Convert the traceback to a string
                error_message = traceback.format_exc()
                # Send to the LLM for debugging and reflection
                responses = send_to_llm_for_debugging(function_content, inputs, error_message, reflections, additional_context)
                # Log the responses to a file
                # if output does not exist, create it
                with open(output, "w") as file:
                    file.write(f"Function `{func.__name__}` raised an exception:\n{error_message}\n")
                    for idx, response in enumerate(responses, 1):
                        file.write(f"LLM Reflection {idx}:\n{response}\n")
                    file.write("----------\n")
                raise  # Re-raise the exception after logging

        return wrapper

    return decorator


def send_to_llm_for_debugging(function_content, inputs, error_message, reflections, additional_context):
    prompt = (f"Debug the following error:\n{error_message}\nin the function:\n{function_content}\n"
              f"with inputs:\n{inputs}\nInclude the full updated function in your response.")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    md_responses = []  # Store each response for logging

    for i in range(reflections):
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        response_content = response.choices[0].message['content']
        md_responses.append(response_content)
        messages.append({"role": "assistant", "content": response_content})
        prompt = "Reflect on your previous answer and provide any corrections or additional insights if necessary."

    return md_responses

def llm_improve(output='improved_function.md', additional_context=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Get the content of the function (source code)
                function_content = inspect.getsource(func)

                # Send to the LLM for improvement suggestions
                improvement_response = send_to_llm_for_improvement(function_content, additional_context)
                
                # Log the improved function to a file
                with open(output, "w") as file:
                    file.write(f"Original function `{func.__name__}`:\n{function_content}\n\n")
                    file.write(f"LLM Improvement Suggestions:\n{improvement_response}\n")
                    file.write("----------\n")

                # Execute the original function
                return func(*args, **kwargs)

            except Exception as e:
                print(f"Exception: '{e}'")
                raise  # Re-raise the exception

        return wrapper

    return decorator

def send_to_llm_for_improvement(function_content, additional_context):
    print("Sending to LLM for improvement suggestions")
    prompt = (f"Improve the following function for better readability, efficiency, and include type hinting:\n"
              f"{function_content}\n{additional_context}")

    messages = [
        {"role": "system", "content": "You are a programming expert."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    response_content = response.choices[0].message['content']

    return response_content

# Example usage
#@llm_improve()
#def sample_function(x, y):
#    return x + y

# Running the sample_function
#sample_function(5, 3)
#Example usage with reflection parameter
#@llm_debugger(reflections=2)
#def test_function(x):
#    return 10 / x  # This will raise a ZeroDivisionError when x is 0
#
## Running the test_function with an argument that causes an error
#try:
#    test_function(0)
#except ZeroDivisionError:
#    pass  # Exception has already been caught, logged, and printed by decorator
def llm_implement(output='completed_function.md'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Get the content of the function (source code) and its docstring
                function_content = inspect.getsource(func)
                docstring = inspect.getdoc(func)

                if not docstring:
                    raise ValueError("Function must have a docstring for llm_implement to work.")

                # Send to the LLM for completion
                completion_response = send_to_llm_for_completion(docstring)

                # Log the completed function to a file
                with open(output, "w") as file:
                    file.write(f"Incomplete function `{func.__name__}`:\n{function_content}\n\n")
                    file.write(f"LLM Completion Based on Docstring:\n{completion_response}\n")
                    file.write("----------\n")

                # Note: The actual function execution is not replaced, 
                # this is just for generating the completed version.
                return func(*args, **kwargs)

            except Exception as e:
                print(f"Exception: '{e}'")
                raise  # Re-raise the exception

        return wrapper

    return decorator

def send_to_llm_for_completion(docstring):
    print("Sending to LLM for function completion based on docstring")
    prompt = (f"Complete the following function based on its docstring:\nDocstring:\n{docstring}\nFunction implementation:")

    messages = [
        {"role": "system", "content": "You are a code generation expert."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    response_content = response.choices[0].message['content']

    return response_content

# Example usage
#@llm_implement()
#def sample_function(x, y):
#    """
#    Add two numbers and return the result.
#    """
#    pass  # Incomplete implementation

# Running the sample_function
#sample_function(5, 3)
