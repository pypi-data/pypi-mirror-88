import re
from .Stack import *

priority = ['*', '/', '+', '-']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def parseFloat(string: str) -> int:
    if string.isdigit():
       return float(string)
    else:
        try:
            return float(string)
        except ValueError:
            return None

def parse(string: str):
    rawString = string.replace(" ", "")
    stack = Stack()
    localExpression = ""
    
    mul = re.compile(r"(.*?)((-?\d*(\.\d+)?)[*](-?\d*(\.\d+)?))")
    div = re.compile(r"(.*?)((-?\d*(\.\d+)?)/(-?\d*(\.\d+)?))")
    add = re.compile(r"(.*?)((-?\d*(\.\d+)?)\+(-?\d*(\.\d+)?))")
    sub = re.compile(r"(.*?)((-?\d*(\.\d+)?)-(-?\d*(\.\d+)?))")

    while True:
        if '*' in rawString:
            groups = re.match(mul, rawString)
            number1 = parseFloat(groups.group(3))
            number2 = parseFloat(groups.group(5))
            result = number1 * number2
            rawString = re.sub(mul, r"\g<1>" + str(result), rawString, count=1)
            rawString = re.sub(r"--", "+", rawString)
        elif '/' in rawString:
            groups = re.match(div, rawString)
            number1 = parseFloat(groups.group(3))
            number2 = parseFloat(groups.group(5))
            result = number1 / number2
            rawString = re.sub(div, r"\g<1>" + str(result), rawString, count=1)
            rawString = re.sub(r"--", "+", rawString)
        elif '+' in rawString:
            groups = re.match(add, rawString)
            number1 = parseFloat(groups.group(3))
            number2 = parseFloat(groups.group(5))
            result = number1 + number2
            rawString = re.sub(add, r"\g<1>" + str(result), rawString, count=1)
            rawString = re.sub(r"--", "+", rawString)
        elif '-' in rawString:
            groups = re.match(sub, rawString)
            number1 = parseFloat(groups.group(3))
            number2 = parseFloat(groups.group(5))
            result = number1 - number2
            rawString = re.sub(sub, r"\g<1>" + str(result), rawString, count=1)
            rawString = re.sub(r"--", "+", rawString)
        if not parseFloat(rawString) == None:
            break
    return parseFloat(rawString)

if __name__ == "__main__":
    print(parse(""))