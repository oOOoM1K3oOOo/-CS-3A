#   Problem: Create Simple Calculator
#   Description: The program computes the complex mathematical expressions with multiple
#       operands which can be a number, a mathematical function, or a factorial. 
#       After the user enters the mathematical expression, the program validates and
#       evaluates the user entry with the regular expressions set in the Calculator 
#       class. If the expression was found to be valid, the program then computes and
#       stores the result inside the Calculator class and prints it to the console. 
#       In addition, the Calculator class stores the value of the memory cell that is
#       accessed through the memory commands (M+, M-, MC, and MR).
#   
#   Name: Mykhaylo Ignatyev
#   ID : 20359765
#   Status: 100% Complete
import math
import re

def main() :    
    entry = ""

    calc = Calculator()
    
    print("This program is a calculator which computes simple mathematical")
    print("expressions and functions.") 
    print()
    print("* For the information about legal syntax and supported functions write")
    print("* \"help\" in the command line.")
    print()
    print("* To exit from the calculator, write \"quit\" in the command line.")
    print()

    calc.help()

    while entry != "quit" :
        entry = input("[x = %s]: " % calc.getX())

        if len(entry) != 0 and entry != "quit" :
            if entry == "help" :
                calc.help()
            else :
                try : 
                    calc.compute(entry)
                except ZeroDivisionError as exception :
                    print()
                    print(str(exception))
                    print()
                except ValueError as exception :
                    print()
                    print(str(exception))
                    print()
                except OverflowError as exception :
                    print()
                    print(str(exception))
                    print()
                except OSError as exception : 
                    print()
                    print(str(exception))
                    print()

## A calculator which computes simple mathematical expressions and functions
#    
class Calculator :
    # Regular expression for matching arithmetic operations. First operand  
    # (\d+|[xXe]|[pP][iI]) (operand1) could be the number or x (previous result), or e,   
    # or Pi, second group ([-+/*^%]) (operator) is the operator, the third 
    # (\d+|[xXe]|[pP][iI]) (operand2) - the number, or x, or e, or Pi.
    REGULAR_MATH = r"(?P<operand1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))\s*" + \
                    r"(?P<operator>[-+/*^%])\s*" + \
                    r"(?P<operand2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))"   

    # Regular expression for matching functions. First group (func) is the function name  
    # (function name (\w+)), second group (\d+|[xXe]|[pP][iI]) (arg1) - the first  
    # argument, the third group (\d+|[xXe]|[pP][iI]) (arg2) – the second argument.
    REGULAR_FUNC = r"(?P<func>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
                    r"\s*[,]?\s*(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\)"
    
    # Regular expression for matching factorials. (\d+) represents the number.
    REGULAR_FACT = r"(?P<factNum>\d+)!"

    # Regular expression for matching arithmetic operations whose operands can be
    # mathematical functions or factorials. First group of the expression is the 
    # first operand that is either a function (func1), a number (operand1, 
    # which could also be x (previous result), or e, or Pi), or a factorial (factNum1).
    # The second group ([-+/*^%]) (operator) is the operator whereas the third group  
    # (\d+|[xXe]|[pP][iI]) (operand2) is either a function (func2), a number (operand2
    # which could also be x, or e, or Pi), or a factorial (factNum2).
    REGULAR_ARITHM = r"(((?P<func1>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|" + \
            r"[xXe]|[pP][iI]))\s*[,]?\s*" + \
            r"(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum1>\d+)!)|" + \
            r"(?P<num1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))\s*" + \
            r"(?P<operator>[-+/*^%])?\s*" + \
            r"(((?P<func2>\w+)\s*\(\s*(?P<arg3>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
            r"\s*[,]?\s*(?P<arg4>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum2>\d+)!)|" + \
            r"(?P<num2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))?"
    
    # Regular expression for matching complex arithmetic operations whose operands can 
    # be mathematical functions or factorials and whose order is defined by the 
    # parentheses. First group of the expression (memOper) is the pattern for matching 
    # memory operations. The second group (parLeft) is an optional opening parentheses
    # which define the order of the mathematical operations. The third group ([-+/*^%])
    # (operator), optional, is the operator whereas the fourth – an operand that is a
    # number (operand, which could also be x (previous result), or e, or Pi). The fifth 
    # group (var) a is a function name that will be added to the mathematical expression
    # stack. The sixth group (comma) is the optional comma to account the complex
    # arguments for the log(), round(), and arbt() functions. The seventh group 
    # (parRight) is an optional closing parentheses whereas the eigth group 
    # (factOper) is an optional factorial sign to account factorial expressions
    REGULAR_COMPLX_MATH = r"((?P<memOper>M[+-RC])(\s*)?)|" + \
            r"(((?P<operator>[-+/*^%])\s+)?" + \
            r"((?P<parLeft>\(+)\s*)?" + \
            r"((?P<num>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))|" + \
            r"(?P<var>\w+))\s*" + \
            r"(?P<parRight>\)+)?" + \
            r"(?P<comma>,)?" + \
            r"(?P<factOper>!)?)"

    # Regular expression for matching memory operations. "M([+-RC])" - results in 
    # adding and substracting the value to the memory cell, recalling and clearing 
    # the value stored in the memory cell
    REGULAR_MEM = r"M([+-RC])"

    # A list of mathematical function which contains the mathematical function names as 
    # a key and executable functions with parameters as the values for those keys 
    FUNCTIONS = {
        "sin" : lambda arg1: math.sin(arg1),
        "csc" : lambda arg1: 1 / math.sin(arg1),
        "cos" : lambda arg1: math.cos(arg1),
        "sec" : lambda arg1: 1 / math.cos(arg1),
        "tan" : lambda arg1: math.tan(arg1),
        "cot" : lambda arg1: 1 / math.cot(arg1),
        "arcsin" : lambda arg1: math.asin(arg1),
        "arccos" : lambda arg1: math.acos(arg1),
        "arctan" : lambda arg1: math.atan(arg1),
        "sqrt" : lambda arg1: math.sqrt(arg1),
        "log" : lambda arg1, arg2: math.log(arg1, arg2),
        "ln" : lambda arg1: math.log(arg1),
        "round" : lambda arg1, arg2: round(arg1, int(arg2)),
        "rad" : lambda arg1: math.radians(arg1),
        "deg" : lambda arg1: math.degrees(arg1),
        "bin" : lambda arg1: bin(int(arg1)),
        "hex" : lambda arg1: hex(int(arg1)),
        "neg" : lambda arg1: (-1) * arg1,
        "abrt" : lambda arg1, arg2: arg1 ** (1 / arg2),
        }

    # Precedence of operators in a mathematical expression
    OPERATOR_PREC = {"(": 1, "+": 2, "-" : 2, "*" : 3, "/": 3, "%" : 3, "^": 4, "!" : 5}

    ## Creates the stored result and memory cell
    #  @param self reference to the instance of a class
    #
    def __init__(self) :
        self._x = 0.0         # Stored result
        self._memory = 0.0    # Memory cell

        # Compiles the regex pattern for complex arithmetic expressions
        self._reComplx = re.compile(self.REGULAR_COMPLX_MATH)

    ## Computes the mathematical expression 
    #  @param entry mathematical expression
    #  @return result of the mathematical expression
    #
    def compute(self, entry) :
        result = 0.0
        mathExp = []        # Dictionary of a mathematical expression

        if self._reComplx.match(entry) :
            # Retrieve the mathematical expression converted to a list
            mathExp = self.retrieveExprList(entry)

            if len(mathExp) >= 2 :
                isTwoArgs = False 

                operands = []

                # Convert the mathematical expression (in infix notaion) to reverse 
                # Polish (postfix) notation 
                mathExp = self.convertToPolish(mathExp)
                
                for elem in mathExp:
                    # Add the operand to the operand stack if it is a number
                    if elem not in self.OPERATOR_PREC and elem not in self.FUNCTIONS and \
                        elem != ",":
                        operands.append(elem)
                    elif elem in self.OPERATOR_PREC :
                        if elem == "!" :
                            # Retrieve the number for factorial function
                            factNum = operands.pop()

                            # Add the result of the factorial operation to the operands stack
                            operands.append(self.calcFact(factNum))
                        else :
                            # Retrieve the first and second operand of the arithmetic expression
                            rightValue = operands.pop()
                            leftValue = operands.pop()

                            # Add the result of the arithmetic operation to the operand stack
                            operands.append(self.calcArithmExpr(leftValue, elem, rightValue))
                    # Raise the flag that two numbers need to be drawn from the operand 
                    # stack for the computation of mathematical function
                    elif elem == "," :
                        isTwoArgs = True
                    else :
                        arg2 = None 

                        # Verify that the function has two arguments in the mathematical
                        # expression list
                        if isTwoArgs :
                            # Retrieve the second argument of the function
                            arg2 = operands.pop()
                            
                            # Clear the flag for retrieving two arguments from the list
                            isTwoArgs = False

                        # Retrieve the first argument of the function
                        arg1 = operands.pop()
                        
                        # Add the result of the function with two agruments to the 
                        # operand stack
                        operands.append(self.calcFunc(elem, arg1, arg2))
    
                result = operands.pop()
                self._x = result
            elif len(mathExp) > 0 :
                self.printMessages("Error: The size of the expression is smaller " + \
                                   "than minimum (2).")
        else :
            self.printMessages("Error: Unknown format of the expression: %s" % entry)

        return result
    
    ## Parses through the mathematical expression and converts it to a list of 
    ## operands and operators
    #  @param self reference to the instance of a class
    #  @param entry mathematical expression
    #  @return list of operands and operators
    #
    def retrieveExprList(self, entry) :
        endPos = 0
        isNotValidEntry = False
        varName = ""
        mathExp = []

        # Find the starting position of the first match
        startPos = self._reComplx.match(entry).start()

        if startPos == 0 :
            for item in self._reComplx.finditer(entry) :
                # Find the ending position of the last match
                endPos = item.end()

                # Retrieve the dictionary with the named subgroups of the match
                token = item.groupdict()
                
                # Verify if the matched string matches pattern for memory operations
                if token["memOper"] is not None :
                    # Perform the memory operation with the given operation name 
                    self.performMemOper(token["memOper"])
                else :

                    # Verify if the operator is present in the expression
                    if token["operator"] is not None : 
                        # Add the operator to the mathematical expression stack
                        mathExp.append(token["operator"])

                    # Verify if the opening parentheses are present in the expression
                    if token["parLeft"] is not None :
                        for pos in range(len(token["parLeft"])) :
                            # Add the opening parentheses to the mathematical expression stack
                            mathExp.append(token["parLeft"][pos])

                    # Verify if a number are present in the expression
                    if token["num"] is not None :
                        # Convert the value of key num1 in dictionary to float
                        operand = self.convertToFloat(token["num"])

                        # Add the number to the mathematical expression stack
                        mathExp.append(operand)
                    # Verify if a function name of complex expression are present in the 
                    # expression
                    elif token["var"] is not None :
                        # Verify if a function name is included in the dictionary of 
                        # functions
                        if token["var"] in self.FUNCTIONS :
                            # Store the function name for further comma validation
                            varName = token["var"]

                            # Add the function name to the mathematical expression stack
                            mathExp.append(token["var"])
                        else :
                            raise ValueError("Error: Unknown operand or function " + \
                                             "name: %s" % token["var"])
                    
                    # Verify if the closing parentheses are present in the expression
                    if token["parRight"] is not None :
                        for pos in range(len(token["parRight"])) :
                            # Add the closing parentheses to the mathematical expression stack
                            mathExp.append(token["parRight"][pos])

                    # Verify if a comma is present in the current match
                    if token["comma"] is not None :
                        # Verify if the function is not a function which takes two arguments
                        if varName not in "log:round:abrt" :
                            # Raise the flag for improper comma placement
                            isNotValidEntry = True
                        else : 
                            isNotValidEntry = False
                        
                        # Clear variable which stores the function name
                        varName = ""

                        # Add comma to the mathematical expression stack if the entry 
                        # was valid
                        if not isNotValidEntry : 
                            mathExp.append(token["comma"])

                    # Verify if the factorial sign for the complex expression is present
                    # in the expression
                    if token["factOper"] is not None :
                        # Add the factorial sign to the mathematical expression stack
                        mathExp.append(token["factOper"])
        
        # Verify that the starting and ending positions of the mathematical expression
        # match the start and end of the entry, respectively
        if isNotValidEntry or not self.isValidMathExp(mathExp) or (startPos > 0 and 
                                                               endPos < len(entry)) :
            # Clear the mathematical expression stack
            mathExp.clear()

            self.printMessages("Error: Unknown input: %s" % entry, 
                               "       Enter \"help\" for guidelines.")

        return mathExp

    ## Calculates the arithmetic expression
    #  @param num1 first operand
    #  @param operator function operator
    #  @param num2 second operand (None when factorial is computed)
    #  @return result of mathematical operation 
    #
    def calcArithmExpr(self, num1, operator, num2 = None) :
        result = self._x

        match operator : 
            case "+":  
                result = num1 + num2
            case "-":  
                result = num1 - num2
            case "*":  
                result = num1 * num2
            case "/":  
                if num2 == 0 :
                    raise ZeroDivisionError("Error: Second operand is zero.")
                
                result = num1 / num2
            case "^":  
                result = num1 ** num2
            case "%":  
                if num2 == 0 :
                    raise ZeroDivisionError("Error: Second operand is zero.")

                result = num1 % num2
            case "!" : 
                # Verify that the number is a whole number
                if not self.isIntegerNum(num1) :
                    raise ValueError("Error: the number for factorial must be a whole number.")
                
                result = self.calcFact(num1)
            case None : 
                result = num1
            case _:
                self.printMessages("Error: Invalid operator: %s" % operator)
        
        return result
    
    ## Calculates factorial of a number
    #  @param self reference to the instance of a class
    #  @param num a whole number
    #
    def calcFact(self, num) :      
        return num * self.calcFact(abs(num) - 1) if abs(num) != 0 else 1 
    
    ## Evaluates and calculates the value of mathematical function with given parameters
    #  @param self reference to the instance of a class
    #  @param function mathermatical function
    #  @param num1 first argument of the function
    #  @param num2 second argument (used for log and arbitrary root functions)
    #  @return result of mathematical operation 
    #
    def calcFunc(self, function, num1, num2 = None) :
        result = self._x

        if function in self.FUNCTIONS :
            match function :
                case "csc" :
                    # Verify that the number does not equal to Pi * n
                    if (math.pi - num1) % math.pi <= 0.01 :
                        raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")

                    result = self.FUNCTIONS[function](num1)
                case "sec" :
                    # Verify that the number does not equal to Pi * ((1/2) + n)
                    if (math.pi * ((1 / 2) + round(num1 / math.pi)) - num1) <= 0.01 :
                        raise ZeroDivisionError("Error: secant is undefined at Pi * ((1/2) + n).")

                    result = self.FUNCTIONS[function](num1)
                case "cot" :
                    # Verify that the number does not equal to Pi * n
                    if (math.pi - num1) % math.pi <= 0.01 :
                        raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")

                    result = self.FUNCTIONS[function](num1)
                case "log":
                    if num2 is None :
                        num2 = 10

                    result = self.FUNCTIONS[function](num1, num2)
                case "ln": 
                    result = math.log(num1)
                case "round" :
                    if num2 is None :
                        num2 = 2
                    elif not self.isIntegerNum(num2) :
                        raise ValueError("Error: the second agrument for round() " +  
                                         "function must be an integer.")

                    result = self.FUNCTIONS[function](num1, num2)
                case "bin" : 
                    if not self.isIntegerNum(num1) :
                        raise ValueError("Error: the number for bin() function must" +
                                         "be an integer.")
                    
                    result = self.FUNCTIONS[function](num1)
                case "hex" : 
                    if not self.isIntegerNum(num1) :
                        raise ValueError("Error: the number for hex() function must" +
                                         "be an integer.")
                    
                    result = self.FUNCTIONS[function](num1)
                case "abrt":
                    if num2 is None :
                        raise ValueError("Error: no second argument was passed to abrt() function.")
                    elif num2 == 0 :
                        raise ZeroDivisionError("Error: second argument of abrt() function is zero.")

                    result = self.FUNCTIONS[function](num1, num2)
                case _:
                    result = self.FUNCTIONS[function](num1)
        else : 
            self.printMessages("Error: Invalid expression: %s" % function)
            
        return result
    
    ## Performs operations with the memory cell:
    ##     - M+ adds the last result to the memory cell
    ##     - M- subtracts the last result from the memory cell
    ##     - MR reads the value from the memory cell
    ##     - MC clears the memory cell
    #  @param self reference to the instance of a class
    #  @param operation memory operation
    #
    def performMemOper(self, operation) : 
        match operation :
            case "M+" : 
                self._memory += self._x
            case "M-" :
                self._memory -= self._x
            case "MC" : 
                self._memory = 0
            case "MR" : 
                self.printMessages("M: %s" % self._memory)
            case _: 
                self.printMessages("Error: Invalid memory operation: %s" % operation)

    ## Converts the value of a string to float
    #  @param self reference to the instance of a class
    #  @param val string to resolve
    #  @return float-point value of val
    #
    def convertToFloat(self, val) :
        num = 0.0 

        match val :
                case "x" | "+x" | "X" | "+X" : 
                    num = self._x
                case "-x" | "-X" : 
                    num = (-1) * self._x
                case "pi" | "+pi" | "pI" | "+pI" | "Pi" | "+Pi" | "PI" | "+PI" : 
                    num = math.pi
                case "-pi" | "-pI" | "-Pi" | "-PI" : 
                    num = (-1) * math.pi
                case "e" | "+e": 
                    num = math.e
                case "-e" : 
                    num = (-1) * math.e
                case None : 
                    num = None
                case _: 
                    num = float(val) 
        
        return num
    
    ## Validates that the mathematical expression follows the mathematical rules
    #  @param self reference to the instance of a class
    #  @param mathExp mathematical expression
    #  @return True if the mathematical expression is syntactically correct else False
    #
    def isValidMathExp(self, mathExp) :
        isValidExpr = True         # Flag for verification of the math expression 
        isFuncFirstArg = False     # Flag to account an argument for function
        isFuncSecArg = False       # Flag to account second argument for function
        isComma = False            # Flag to account a comma before the second argument

        for pos in range(1, len(mathExp)) :
            # If the previous element of the expression is a function, raise the flag
            # for the first argument
            if mathExp[pos - 1] in self.FUNCTIONS :
                isFuncFirstArg = True

                # If a function can take two arguments, raise the flag for the comma and
                # the second argument
                if mathExp[pos - 1] in "log:round:abrt" :
                    isComma = True
                    isFuncSecArg = True

            # If the flag for the first argument is raised and the current element of 
            # the expression is a function or a number, clear the flag
            if isFuncFirstArg and (mathExp[pos] in self.FUNCTIONS or 
                              self.isFloatNum(mathExp[pos])) :
                isFuncFirstArg = False

            # If the flag for the comma is raised and the current element of the 
            # expression is a comma, clear the flag
            if isFuncSecArg and isComma and mathExp[pos] == "," :
                isComma = False

            # If the flag for the second argument is raised and the current element of
            # the expression is a function or a number, clear the flag
            if not isFuncFirstArg and not isComma and isFuncSecArg and (
                mathExp[pos] in self.FUNCTIONS or self.isFloatNum(mathExp[pos])) :
                isFuncSecArg = False

            #if isFuncSecArg and mathExp[pos] == ","
                

            # Verify if the mathematical expression follows common syntactical errors
            if ((mathExp[pos] in self.FUNCTIONS or self.isFloatNum(mathExp[pos])) and 
                    (self.isFloatNum(mathExp[pos - 1]) or mathExp[pos - 1] == ")")) or (
                    mathExp[pos - 1] in self.OPERATOR_PREC and 
                    mathExp[pos - 1] != "(" and pos == 1) or (
                    mathExp[pos] in self.FUNCTIONS and pos == len(mathExp) - 1) or (
                    mathExp[pos - 1] == "(" and mathExp[pos] == ",") or (
                    mathExp[pos - 1] in self.FUNCTIONS and mathExp[pos] != "(") or (
                    isFuncFirstArg and mathExp[pos] in self.OPERATOR_PREC and 
                    mathExp[pos] != "(") or (
                    not isFuncSecArg and mathExp[pos] == ",") or (
                    isFuncFirstArg and mathExp[pos] == ",") or (
                    isFuncSecArg and mathExp[pos - 1] == "," and 
                    mathExp[pos] in self.OPERATOR_PREC and mathExp[pos] != "(") :
                isValidExpr = False
        
        return isValidExpr
    
    ## Converts the arithmetic expression to reverse Polish notation
    #  @param self reference to the instance of a class
    #  @param arithmExpr original arithmetic expression
    #  @return list of operands and operators in reverse Polish notation
    #
    def convertToPolish(self, arithmExpr) :
        mathExp = []
        operatorStack = []

        for elem in arithmExpr :
            # Verify that the element of the expression is the function name
            if elem in self.FUNCTIONS :
                # Add the function name to the operator stack
                operatorStack.append(elem)
            # Verify that the element of the expression is the opening parentheses 
            elif elem == "(" :
                # Add the opening parentheses to the operator stack
                operatorStack.append(elem)
            # Verify that the element of the expression is the closing parentheses 
            # or a comma
            elif elem == ")" or elem == "," : 
                # While the operator stack is not empty and the last element of the stack 
                # is an operator, add the operator from the operator stack to the new list for 
                # mathematical expression in reverse Polish notation
                while len(operatorStack) > 0 and (operatorStack[-1] not in self.FUNCTIONS and operatorStack[-1] != "(" ):
                    mathExp.append(operatorStack.pop())
                
                # Pop the opening parentheses from the operator stack if the operator 
                # stack is not empty and the element of the exppresion is not a comma
                if len(operatorStack) > 0 and elem != ",":
                    operatorStack.pop()

                if elem == "," :
                    mathExp.append(elem)

                # Add the function name from the operator stack to the new list for 
                # mathematical expression if the operator stack is not empty and
                # the last element of the stack is a function name
                if len(operatorStack) > 0 and operatorStack[-1] in self.FUNCTIONS and elem != ",":
                    mathExp.append(operatorStack.pop())
            # Verify that the element of the expression is an operator
            elif elem in self.OPERATOR_PREC :
                # While the operator stack is not empty and the current operator of the 
                # expression has lower or equal precedence than the last element of the
                # operator stack, add the last operator from the operator stack to the 
                # new list for mathematical expression in reverse Polish notation   
                while len(operatorStack) > 0 and self.OPERATOR_PREC[elem] <= self.OPERATOR_PREC[operatorStack[-1]] :
                    mathExp.append(operatorStack.pop())
                
                # Add the current operator to the operator stack
                operatorStack.append(elem)
            # Verify that the element of the expression is a number       
            else :  
                # Add to the new list for mathematical expression in reverse Polish
                # notation             
                mathExp.append(elem)

        # If the operator stack is not empty and the element is not the opening 
        # parentheses, add the operators from the operator stack to the new list for 
        # mathematical expression in reverse Polish notation
        while len(operatorStack) > 0 :
            operator = operatorStack.pop()

            if operator != "(" :
                mathExp.append(operator)
    
        return mathExp
    
    ## Validates that the string is a rational number
    #  @param self reference to the instance of a class
    #  @param entry a string
    #  @return True if the string is a rational number else False
    #
    def isFloat(self, entry) :
        isValidEntry = False
        startPos = 0

        # Verify that the string is not empty
        if len(entry) > 0 :
            # Verify that the string starts with +- and increment the starting pos by 1
            if entry.startswith("+-") :
                startPos = 1

            # Find the position of the first point
            pointPos = entry.find(".")

            # If the point is not found, verify that the string from start pos is 
            # an integer
            if pointPos == -1 and entry[startPos : ].isdigit() :
                isValidEntry = True
            # If the point was found, verify that the substrings divided by the point
            # are integers 
            elif pointPos >= 0 and entry[startPos : pointPos].isdigit() and entry[pointPos + 1 : ].isdigit() : 
                isValidEntry = True

        return isValidEntry
    
    ## Validates that the number is a rational number
    #  @param self reference to the instance of a class
    #  @param num a number
    #  @return True if num is a rational number else False
    def isFloatNum(self, num) :
        return isinstance(num, float)
    
    ## Validates that the string is an integer
    #  @param self reference to the instance of a class
    #  @param entry a string
    #  @return True if the string is an integer else False
    #
    def isInteger(self, entry) :
        isValidEntry = False

        if len(entry) != 0 :
            # Verify that the string starts with +- and increment the starting pos by 1
            startPos = 1 if entry.startswith("+-") else 0
            
            # Verify that the string from start pos is an integer
            if entry[startPos : ].isdigit() :
                isValidEntry = True
        
        return isValidEntry
    
    ## Validates that the number is a whole number
    #  @param self reference to the instance of a class
    #  @param num a number
    #  @return True if the number is a whole number else False
    #
    def isIntegerNum(self, num) :    
        return num % 1 == 0
    
    ## Retrieves the value of variable x
    #  @return value of x
    #
    def getX(self) :
        return self._x
    
    ## Retrieves the value in the memory cell
    #  @return value in the memory cell
    #
    def getMemoryVal(self) :
        return self._memory
    
    ## Prints a passed message
    #  @param self reference to the instance of a class
    #  @param *messages tuple containing all passed messages
    #  
    def printMessages(self, *messages) :
        print()

        if len(messages) != 0 :
            for message in messages :
                print(message)

        print()

    ## Provides information about the functionality of the Calculator class
    #  @param self reference to the instance of a class
    #
    def help(self) :
        print()
        print("Supported functions:")
        print("\t\t* Note: All operators and operands should be separated by a space.")
        print("\t- Addition: Number + Number")
        print("\t- Subtraction: Number - Number")  
        print("\t- Multiplication: Number * Number") 
        print("\t- Division: Number / Number") 
        print("\t- Modulus: Number % Number") 
        print("\t- Exponents: Number ^ Number") 
        print("\t- Factorial: Number!") 
        print("\t\t* Note: \"Number\" must be a whole number.")
        print("\t- Trigonometric functions (sin, cos, tan, arctan, etc.): sin(Number)")
        print("\t\t* Note: Default units for the angle is in Radians (Rad).")
        print("\t\t* Note: \"Pi\" is the variable for Pi.")
        print("\t- Square root: sqrt(Number)") 
        print("\t- Arbitrary roots: abrt(Number, Number)") 
        print("\t- Logarithms: log(Number); ln(Number)")
        print("\t\t * Note: The default base for log() function is 10.")
        print("\t- Negation: neg(Number)") 
        print("\t- Rounding: round(Number)")
        print("\t\t * Note: Rounds the number to 2 decimal places by default.")
        print("\t- Angles in degrees or radians: deg(Number); rad(Number)") 
        print("\t- Conversion from base 10 to binary (for integers only): bin(Number)")
        print("\t- Previous result used as first operand: x + Number")
        print("\t- The ability to store and recall results: M+; M-; MR; MC") 
        print()
    
if __name__ == "__main__" :
    main()