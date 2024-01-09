Incomplete function `sample_implement`:
@llm_implement(output='completed_function.md')
def sample_implement(x, y):
    '''
    calculate celsius to fahrenheit
    
    '''
    pass


LLM Completion Based on Docstring:
Certainly! Below is the Python function that converts Celsius to Fahrenheit, as described by the docstring:

```python
def celsius_to_fahrenheit(celsius):
    """
    Convert a temperature given in Celsius to Fahrenheit.

    :param celsius: The temperature in degrees Celsius.
    :return: The temperature in degrees Fahrenheit.
    """
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit
```

This function takes as input the temperature in degrees Celsius, applies the conversion formula to get the temperature in degrees Fahrenheit, and then returns the result.
----------
