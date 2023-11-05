
```markdown
# LLM Debugger

LLM Debugger is a Python package that uses OpenAI's GPT-4 model to debug Python code. When a function decorated with `@llm_debugger` raises an exception, the function's source code and the traceback are sent to the language model for debugging. The model's responses are then logged to a file.

## Installation

To install the package, navigate to the package directory and run:

```bash
pip install .
```

## Usage

Here's an example of how to use the `llm_debugger` decorator in your code:

```python
from llm_debug import llm_debugger

@llm_debugger(reflections=3, output='error_response.md')
def buggy_function():
    # Some buggy code here...
    pass
```

In this example, if `buggy_function` raises an exception, the exception and the function's source code will be sent to the language model for debugging. The model's responses will be logged to `error_response.md`.

## Environment Variables

The package requires the `OPENAI_API_KEY` environment variable to be set. You can set this in a `.env` file in the same directory as your script:

```env
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your actual OpenAI API key.
```
