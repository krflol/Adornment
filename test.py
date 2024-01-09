from adornment.adornment import llm_debugger, llm_improve, llm_implement
import datetime


timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
@llm_debugger(reflections=2, output=f'sample_debug_{timestamp}.md')
def sample_debug(x):
    return 10 / x  # This will raise a ZeroDivisionError when x is 0

# Running the test_function with an argument that causes an error
try:
    sample_debug(0)
except ZeroDivisionError:
    pass

#@llm_improve()
#def sample_improve(x, y):
#    #calculate celsius to fahrenheit
#    celsius = (x + y) / 2
#    fahrenheit = (celsius * 9/5) + 32
#    return fahrenheit
#
#sample_improve(5, 3)

#@llm_implement(output='completed_function.md')
#def sample_implement(x, y):
#    '''
#    calculate celsius to fahrenheit
#    
#    '''
#    pass
#
#sample_implement(5, 3)