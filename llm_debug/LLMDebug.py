import os
import traceback
import inspect
from functools import wraps
from dotenv import load_dotenv
from langchain.llms import OpenAI
import openai

class LLMDebugger:
    def __init__(self, reflections=1, output='error_response.md'):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4")
        openai.api_key = OPENAI_API_KEY
        self.reflections = reflections
        self.output = output

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Exception:'{e}' being sent to LLM for debugging")
                function_content = inspect.getsource(func)
                error_message = traceback.format_exc()
                responses = self.send_to_llm_for_debugging(function_content, error_message)
                with open(self.output, "w") as file:
                    file.write(f"Function `{func.__name__}` raised an exception:\n{error_message}\n")
                    for idx, response in enumerate(responses, 1):
                        file.write(f"LLM Reflection {idx}:\n{response}\n")
                    file.write("----------\n")
                raise
        return wrapper

    def send_to_llm_for_debugging(self, function_content, error_message):
        prompt = (f"Debug the following error:\n{error_message}\nin the function:\n{function_content}\n"
                  "Include the full updated function in your response.")
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        md_responses = []
        for i in range(self.reflections):
            messages.append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
            response_content = response.choices[0].message['content']
            md_responses.append(response_content)
            messages.append({"role": "assistant", "content": response_content})
            prompt = "Reflect on your previous answer and provide any corrections or additional insights if necessary."
        return md_responses