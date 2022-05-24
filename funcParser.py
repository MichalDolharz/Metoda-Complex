import re
import numpy as np
from typing import Callable, List

replace = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
    'pi' : 'np.pi',
    'abs' : 'np.absolute',
    'tan' : 'np.tan',
    'atan' : 'np.arctan'
}

allowed = {
    'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15',
    'sin',
    'cos',
    'exp',
    'sqrt',
    'pi',
    'abs',
    'tan',
    'atan'
}

#Formatting a user-entered function into a format readable by matplotlib
def getFunction(funcString: str):
    
    #Looking for not allowed expressions. If one is found, an exception is thrown.
    for expr in re.findall('[a-zA-Z_]+[0-9]*', funcString):
        if(expr not in allowed):
            raise Exception(f'{expr} is not allowed in function')

    #Searching for and replacing expressions (i.e. "sin" to "np.sin")
    funcString = re.sub(r"([\d]+)([a-zA-Z_])", r"\1*\2", funcString)
    for toReplace, newValue in replace.items():
        funcString = funcString.replace(toReplace, newValue)
    print(funcString)


    def parsedFun(x1=0, x2=0, x3=0, x4=0, x5=0):

        return eval(funcString)

    

    return parsedFun


def getFunctionString(funcString: str):
    
    #Looking for not allowed expressions. If one is found, an exception is thrown.
    for expr in re.findall('[a-zA-Z_]+[0-9]*', funcString):
        if(expr not in allowed):
            raise Exception(f'{expr} is not allowed in function')

    #Searching for and replacing expressions (i.e. "sin" to "np.sin")
    funcString = re.sub(r"([\d]+)([a-zA-Z_])", r"\1*\2", funcString)
    for toReplace, newValue in replace.items():
        funcString = funcString.replace(toReplace, newValue)
        
    return funcString